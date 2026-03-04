"""Local helper to validate your OpenAI API key is configured.

Usage (do this locally, do NOT paste your key into public chats):

    # Temporarily in your shell
    export OPENAI_API_KEY="sk-REPLACE_WITH_YOUR_KEY"
    python check_key.py

Or create a local .env file containing OPENAI_API_KEY and run the app.

This script will attempt a minimal ChatCompletion call. Only run it locally after you
rotate the leaked key. The script does not store or echo your key.
"""
import os
import sys

try:
    import openai
except Exception:
    print("openai package not installed. Install with: pip install openai")
    sys.exit(2)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    print("No OPENAI_API_KEY found in environment. Set it temporarily with:\n  export OPENAI_API_KEY=your_key_here")
    sys.exit(1)

# Wire the key into the client
openai.api_key = OPENAI_API_KEY

def main():
    print("Attempting a minimal API call — this runs against OpenAI and will use your key.")
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": "Say hello in one word."}],
            max_tokens=5,
            temperature=0.0,
            request_timeout=10,
        )
        choices = resp.get('choices') or []
        if not choices:
            print('No choices returned. The key may be invalid or there was an error.')
            sys.exit(3)
        reply = choices[0].get('message', {}).get('content', '').strip()
        print('API call succeeded. Example reply:', reply)
        sys.exit(0)
    except openai.error.OpenAIError as e:
        print('OpenAI error:', str(e))
        sys.exit(4)
    except Exception as e:
        print('Unexpected error:', str(e))
        sys.exit(5)

if __name__ == '__main__':
    main()
