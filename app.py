import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = 'gemini-flash-latest'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not API_KEY:
        return jsonify({"response": "Error: API Key is missing."})

    data = request.json
    user_message = data.get("message")
    history = data.get("history", [])
    # New Feature: Get the tone from the frontend
    selected_tone = data.get("tone", "Professional")

    # We dynamically build the prompt based on the user's selection
    SYSTEM_PROMPT = f"""
    You are an expert business copywriter.
    Current Tone Setting: **{selected_tone}**
    
    Your Goal: Help the user write perfect WhatsApp Business Templates.
    
    1. If the user asks for a template:
       - Write it in a {selected_tone} style.
       - Structure it with: "Subject", "Category", and "Body".
       - Use variables like {{1}} where needed.
    
    2. If the user just chats (e.g. "Hi", "Help me"):
       - Be helpful and polite, but keep your responses concise.
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"AI Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
