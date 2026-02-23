import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Use a safe default for now, but we will check the list later
# We are removing 'system_instruction' for a moment to ensure basic connection works first
model = genai.GenerativeModel('gemini-1.5-flash') 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def test_connection():
    """This hidden page will list exactly what models your key can use."""
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        return jsonify({"STATUS": "API Connected!", "AVAILABLE_MODELS": available_models})
    except Exception as e:
        return jsonify({"STATUS": "Error", "DETAILS": str(e)})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    try:
        # Simple generation without system instructions for now to test the pipe
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
