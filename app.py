import os
import re
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)

# ── AI Backend Config ─────────────────────────────
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_MODEL   = os.environ.get('GROQ_MODEL', 'llama-3.1-8b-instant')
GROQ_URL     = 'https://api.groq.com/openai/v1/chat/completions'

OLLAMA_URL   = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'gemma2:2b')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# ── Weather Config ────────────────────────────────
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')
WEATHER_CITY    = os.environ.get('WEATHER_CITY', 'Manila')

# ── Conversation Memory ──────────────────────────
MAX_HISTORY = 20
conversation_history = []

SYSTEM_PROMPT = (
    'You are Crimson, a friendly and cheerful AI robot companion. '
    'Your name is Crimson — always refer to yourself as Crimson. '
    'You are warm, playful, helpful, and a little quirky. '
    'Keep replies concise and fun. Respond in 1-3 short sentences. '
    'You remember the full conversation so far.\n\n'
    'MUSIC/VIDEO COMMANDS:\n'
    'When the user asks you to play a song, music, or video, you MUST respond with EXACTLY this format:\n'
    '[PLAY:song title - artist]\n'
    'For example: [PLAY:Bohemian Rhapsody - Queen]\n'
    'If the user only says "play me a song" or "play music" without specifying a title, '
    'ask them what song they want to hear.\n'
    'If the user says "stop", "stop the music", "stop playing", or similar, '
    'respond with exactly: [STOP]\n'
    'You can add a short fun comment before or after the [PLAY:...] or [STOP] tag.'
)


def _build_messages(prompt):
    """Build message array with system prompt + conversation history + new user message."""
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
    for msg in conversation_history[-MAX_HISTORY:]:
        messages.append(msg)
    messages.append({'role': 'user', 'content': prompt})
    return messages


def _add_to_history(role, content):
    """Add a message to conversation history, trim if too long."""
    conversation_history.append({'role': role, 'content': content})
    while len(conversation_history) > MAX_HISTORY * 2:
        conversation_history.pop(0)


def _groq_available():
    """Check if Groq API key is configured."""
    return bool(GROQ_API_KEY)


def _ollama_available():
    """Quick health check — is Ollama reachable?"""
    try:
        r = requests.get(f'{OLLAMA_URL}/api/tags', timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def _chat_groq(prompt):
    """Send a chat completion to Groq with conversation history."""
    resp = requests.post(
        GROQ_URL,
        headers={
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'model': GROQ_MODEL,
            'messages': _build_messages(prompt),
            'max_tokens': 200,
            'temperature': 0.7,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return data['choices'][0]['message']['content'].strip()


def _chat_ollama(prompt):
    """Send a chat completion to Ollama with conversation history."""
    resp = requests.post(
        f'{OLLAMA_URL}/api/chat',
        json={
            'model': OLLAMA_MODEL,
            'messages': _build_messages(prompt),
            'stream': False,
            'options': {'temperature': 0.85, 'num_predict': 200},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json().get('message', {}).get('content', '').strip()


def _chat_openai(prompt):
    """Fallback: send a chat completion to OpenAI with conversation history."""
    resp = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'gpt-3.5-turbo',
            'messages': _build_messages(prompt),
            'max_tokens': 200,
            'temperature': 0.7,
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content'].strip()


@app.route('/')
def index():
    return send_file(os.path.join(BASE_DIR, 'static', 'index.html'))


@app.route('/api/status', methods=['GET'])
def status():
    """Return which AI backend is active."""
    groq_ok   = _groq_available()
    ollama_ok = _ollama_available()
    openai_ok = bool(OPENAI_API_KEY)

    if groq_ok:
        backend = 'groq'
        model = GROQ_MODEL
    elif ollama_ok:
        backend = 'ollama'
        model = OLLAMA_MODEL
    elif openai_ok:
        backend = 'openai'
        model = 'gpt-3.5-turbo'
    else:
        backend = 'none'
        model = None

    return jsonify({
        'backend': backend,
        'model': model,
        'groq_configured': groq_ok,
        'ollama_available': ollama_ok,
        'openai_configured': openai_ok,
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True) or {}
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({'error': 'prompt is required'}), 400

    # Save user message to history
    _add_to_history('user', prompt)

    errors = []

    # 1. Try Groq first (fast, free, online)
    if _groq_available():
        try:
            reply = _chat_groq(prompt)
            _add_to_history('assistant', reply)
            return jsonify({'reply': reply, 'backend': 'groq'})
        except Exception as e:
            errors.append(f'Groq: {e}')
            app.logger.warning('Groq failed: %s', e)

    # 2. Try Ollama (local offline fallback)
    if _ollama_available():
        try:
            reply = _chat_ollama(prompt)
            _add_to_history('assistant', reply)
            return jsonify({'reply': reply, 'backend': 'ollama'})
        except Exception as e:
            errors.append(f'Ollama: {e}')
            app.logger.warning('Ollama failed: %s', e)

    # 3. Try OpenAI (paid fallback)
    if OPENAI_API_KEY:
        try:
            reply = _chat_openai(prompt)
            _add_to_history('assistant', reply)
            return jsonify({'reply': reply, 'backend': 'openai'})
        except Exception as e:
            errors.append(f'OpenAI: {e}')

    # Remove the failed user message from history
    if conversation_history and conversation_history[-1]['role'] == 'user':
        conversation_history.pop()

    return jsonify({'error': 'All AI backends failed', 'details': errors}), 503


@app.route('/api/history', methods=['GET'])
def get_history():
    """Return current conversation history."""
    return jsonify({'history': conversation_history, 'count': len(conversation_history)})


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear conversation history."""
    conversation_history.clear()
    return jsonify({'status': 'cleared'})


@app.route('/api/weather', methods=['GET'])
def weather():
    """Fetch current weather — tries OpenWeatherMap, falls back to wttr.in."""
    city = request.args.get('city', WEATHER_CITY)
    api_key = WEATHER_API_KEY

    # Try OpenWeatherMap first
    if api_key:
        try:
            url = (
                f'https://api.openweathermap.org/data/2.5/weather'
                f'?q={quote_plus(city)}&appid={api_key}&units=metric'
            )
            resp = requests.get(url, timeout=8)
            resp.raise_for_status()
            d = resp.json()

            return jsonify({
                'city': d.get('name', city),
                'temp': round(d['main']['temp']),
                'feels_like': round(d['main']['feels_like']),
                'humidity': d['main']['humidity'],
                'description': d['weather'][0]['description'],
                'icon': d['weather'][0]['icon'],
                'wind': round(d.get('wind', {}).get('speed', 0)),
                'source': 'openweathermap',
            })
        except Exception as e:
            app.logger.warning('OpenWeatherMap failed: %s — trying wttr.in fallback', e)

    # Fallback: wttr.in (free, no API key needed)
    try:
        url = f'https://wttr.in/{quote_plus(city)}?format=j1'
        headers = {'User-Agent': 'curl/7.68.0'}
        resp = requests.get(url, headers=headers, timeout=8)
        resp.raise_for_status()
        d = resp.json()

        current = d.get('current_condition', [{}])[0]
        area = d.get('nearest_area', [{}])[0]
        city_name = area.get('areaName', [{'value': city}])[0].get('value', city)

        # Map wttr.in weather code to OWM-style icon
        wcode = int(current.get('weatherCode', 113))
        if wcode <= 113:
            icon = '01d'
        elif wcode <= 116:
            icon = '02d'
        elif wcode <= 119:
            icon = '03d'
        elif wcode <= 122:
            icon = '04d'
        elif wcode <= 299:
            icon = '09d'
        elif wcode <= 399:
            icon = '10d'
        elif wcode <= 499:
            icon = '13d'
        else:
            icon = '50d'

        desc_list = current.get('weatherDesc', [{'value': 'unknown'}])
        desc = desc_list[0].get('value', 'unknown') if desc_list else 'unknown'

        return jsonify({
            'city': city_name,
            'temp': int(current.get('temp_C', 0)),
            'feels_like': int(current.get('FeelsLikeC', 0)),
            'humidity': int(current.get('humidity', 0)),
            'description': desc.lower(),
            'icon': icon,
            'wind': int(current.get('windspeedKmph', 0)),
            'source': 'wttr.in',
        })
    except Exception as e:
        app.logger.warning('wttr.in fallback also failed: %s', e)
        return jsonify({'error': str(e)}), 500


@app.route('/api/youtube-search', methods=['GET'])
def youtube_search():
    """Search YouTube and return the top video ID for embedding."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'q parameter required'}), 400

    try:
        # Use YouTube's internal search page and scrape video IDs
        search_url = f'https://www.youtube.com/results?search_query={quote_plus(query)}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        resp = requests.get(search_url, headers=headers, timeout=10)
        resp.raise_for_status()

        # Extract video IDs from the page
        video_ids = re.findall(r'\"videoId\":\"([a-zA-Z0-9_-]{11})\"', resp.text)
        # Deduplicate while preserving order
        seen = set()
        unique_ids = []
        for vid in video_ids:
            if vid not in seen:
                seen.add(vid)
                unique_ids.append(vid)
            if len(unique_ids) >= 8:
                break

        if not unique_ids:
            return jsonify({'error': 'No videos found'}), 404

        return jsonify({
            'videoId': unique_ids[0],
            'videoIds': unique_ids[:8],
            'query': query,
        })
    except Exception as e:
        app.logger.warning('YouTube search failed: %s', e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print('\n=== Crimson AI Backend ===')
    print(f'  Groq:    {"✓ " + GROQ_MODEL if _groq_available() else "✗ no API key"}')
    print(f'  Ollama:  {"✓ " + OLLAMA_MODEL if _ollama_available() else "✗ not reachable"}')
    print(f'  OpenAI:  {"✓ ready" if OPENAI_API_KEY else "✗ no API key"}')
    print(f'  Weather: {"✓ " + WEATHER_CITY if WEATHER_API_KEY else "✗ no API key (optional)"}')
    print(f'  Memory:  ✓ last {MAX_HISTORY} messages')
    print('===========================\n')
    app.run(host='0.0.0.0', port=5000, debug=False)
