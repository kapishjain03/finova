import os
from flask import Flask, request, jsonify, send_from_directory
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Constants
SARVAM_KEY = os.environ.get("SARVAM_KEY")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")

@app.route("/")
def index():
    return send_from_directory('../', 'index.html')

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    url = "https://api.sarvam.ai/translate/v1"
    headers = {"Content-Type": "application/json", "api-key": SARVAM_KEY}
    response = requests.post(url, json=data, headers=headers)
    return jsonify(response.json())

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    history = data.get("history", [])
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = history + [{"role": "user", "content": question}]
    
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": messages
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {"Content-Type": "application/json", "api-key": SARVAM_KEY}
    response = requests.post(url, json=data, headers=headers)
    return jsonify(response.json())

@app.route("/stt", methods=["POST"])
def stt():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    language_code = request.form.get('language_code', 'hi-IN')
    
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {"api-key": SARVAM_KEY}
    
    files = {'file': (file.filename, file.stream, file.mimetype)}
    data = {'language_code': language_code}
    
    response = requests.post(url, files=files, data=data, headers=headers)
    return jsonify(response.json())

# Vercel requirements
def handler(request):
    return app(request)

if __name__ == "__main__":
    app.run(port=5000)
