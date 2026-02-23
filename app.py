import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Use the model that works for your account
MODEL_NAME = 'gemini-flash-latest'

# --- NEW INTELLIGENT PERSONA ---
SYSTEM_PROMPT = """
You are a friendly, intelligent AI assistant. You can have normal conversations about anything (weather, coding, life, business).

HOWEVER, you have a special talent for writing "WhatsApp Business Templates". 
- If the user asks for a template (or it looks like they need a business message), provide one formatted with:
  1. Template Name (lowercase_underscore)
  2. Category (MARKETING, UTILITY, etc.)
  3. The Message Body (with {{1}} variables).
- If they are just chatting (e.g., "Hi", "How are you"), just reply normally and friendly. 
- You can occasionally (but not always) mention: "By the way, I can help you draft a WhatsApp template if you need one!"
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not API_KEY:
        return jsonify({"response": "Error: API Key is missing."})

    data = request.json
    user_message = data.get("message")
    # We get the history from the browser so the bot remembers the context!
    history = data.get("history", [])

    try:
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)
        
        # We start the chat with the history sent from the frontend
        chat_session = model.start_chat(history=history)
        
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"AI Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
