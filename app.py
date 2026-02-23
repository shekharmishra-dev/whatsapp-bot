import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- CONFIGURATION ---
# We are using the model explicitly listed in your account
MODEL_NAME = 'gemini-2.0-flash' 

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
        # Create the model with the specific system instruction
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)
        
        # Start a chat session (this helps it remember context if needed)
        chat_session = model.start_chat(history=[])
        
        # Send the user's message
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
