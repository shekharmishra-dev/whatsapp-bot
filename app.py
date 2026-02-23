import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURATION ---
# 1. GET API KEY
# We get the key from Render's settings securely
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

# 2. SELECT THE AI MODEL
# We are using this specific name because it appeared in your allowed list.
MODEL_NAME = 'gemini-flash-latest'

# 3. SET THE RULES (SYSTEM PROMPT)
# This tells the AI how to behave (like a WhatsApp expert)
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
    """Renders the main website page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles the chat messages from the user."""
    
    # Security check: Does the API key exist?
    if not API_KEY:
        return jsonify({"response": "Error: API Key is missing. Please add GEMINI_API_KEY to Render Environment Variables."})

    # Get the message the user typed
    user_message = request.json.get("message")
    
    try:
        # Initialize the AI Model
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)
        
        # Start the chat
        chat_session = model.start_chat(history=[])
        
        # Send message and get response
        response = chat_session.send_message(user_message)
        
        # Return the AI's answer to the website
        return jsonify({"response": response.text})
        
    except Exception as e:
        # If anything goes wrong, send the error message back to the chat box
        return jsonify({"response": f"AI Error: {str(e)}"})

if __name__ == '__main__':
    # This is for running locally on your computer
    app.run(debug=True)
