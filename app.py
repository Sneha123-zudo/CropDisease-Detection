from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        uploaded_file = request.files['image']
        if uploaded_file.filename == '':
            return jsonify({'error': 'No file uploaded'}), 400

        # Custom plant disease prompt
        prompt = (
            "You are an expert plant pathologist. Analyze the plant leaf image and return response in this exact format:\n\n"
            "🌿 Disease Name: \n"
            "🩺 Symptoms: \n"
            "💊 Remedies: \n"
            "🛡️ Prevention: \n"
            "✅ Health Status (Healthy/Infected):"
        )

        # Convert uploaded image
        image = Image.open(uploaded_file).convert('RGB')

        # Send prompt and image to Gemini
        result = model.generate_content([prompt, image])
        text = result.text.strip()

        return jsonify({'response': text})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
