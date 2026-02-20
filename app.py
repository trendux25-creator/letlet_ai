import os
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


@app.route('/')
def index():
    return send_file(os.path.join(BASE_DIR, 'static', 'index.html'))


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True) or {}
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({'error': 'prompt is required'}), 400

    if not OPENAI_API_KEY:
        return jsonify({'error': 'Server missing API key'}), 500

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are LetLet, a friendly and cheerful AI companion for a robot. Keep replies concise and fun.'},
            {'role': 'user', 'content': prompt},
        ],
        'max_tokens': 300,
        'temperature': 0.85,
    }

    try:
        resp = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers, json=payload, timeout=20
        )
        j = resp.json()

        # Surface OpenAI error messages clearly (e.g. quota exceeded, invalid key)
        if 'error' in j:
            err = j['error']
            msg = err.get('message', 'Unknown OpenAI error')
            code = err.get('code', err.get('type', 'api_error'))
            return jsonify({'error': f'OpenAI: {msg}', 'code': code}), 502

        resp.raise_for_status()
        reply = j['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except requests.RequestException as e:
        return jsonify({'error': 'Network error reaching OpenAI', 'details': str(e)}), 502


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
