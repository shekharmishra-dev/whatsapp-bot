import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- CONFIGURATION ---
# We are using 'gemini-flash-latest' which was explicitly on your allowed list.
MODEL_NAME = 'gemini-flash-latest'

SYSTEM_PROMPT = """
You are a helpful assistant that writes WhatsApp Business Templates. 
When a user asks for a template, provide:
1. The Template Name (in lowercase with underscores, e.g., order_confirmation)
2. The Template Category (e.g., UTILITY, MARKETING)
3. The Body Text (use {{1}}, {{2}} for variables and *bold* for formatting).
Keep the response clean and easy to copy.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not API_KEY:
        return jsonify({"response": "Error: API Key is missing. Please check Render settings."})

    user_message = request.json.get("message")
    
    try:
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
