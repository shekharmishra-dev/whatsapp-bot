import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# We will use the standard, stable Flash model
# If this fails later, we can try 'gemini-pro'
MODEL_NAME = 'gemini-1.5-flash' 

SYSTEM_PROMPT = """
You are a helpful assistant that writes WhatsApp Business Templates. 
When a user asks for a template, provide:
1. The Template Name (lowercase_with_underscores)
2. The Category (e.g., UTILITY, MARKETING)
3. The Body Text.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Check if API Key exists
    if not API_KEY:
        return jsonify({"response": "Error: API Key is missing. Check Render settings."})

    user_message = request.json.get("message")
    
    try:
        # We initialize the model here so if the name is wrong, 
        # it only errors in the chat, not crash the whole site.
        model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)
        chat = model.start_chat(history=[])
        response = chat.send_message(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"AI Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
