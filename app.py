import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
# We will set the API key securely later on the server
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# This tells the AI how to behave
SYSTEM_PROMPT = """
You are a helpful assistant that writes WhatsApp Business Templates. 
When a user asks for a template, provide:
1. The Template Name (lowercase_with_underscores)
2. The Category (e.g., UTILITY, MARKETING)
3. The Body Text (use {{1}} for variables).
Keep it clean and professional.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-001', system_instruction=SYSTEM_PROMPT)
        chat = model.start_chat(history=[])
        response = chat.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
