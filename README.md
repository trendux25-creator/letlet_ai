# LetLet AI Companion

This project is a lightweight AI companion for a robot. It uses a Flask backend to proxy requests to the OpenAI Chat API and a responsive HTML/CSS/JS frontend that displays animated eyes which adapt to any screen size.

Features
- Responsive, animated eyes UI suitable for an LCD or monitor
- Flask backend that forwards prompts to the Chat API
- Simple chat panel and logs

Setup
1. Copy your API key into an environment variable. Create a file named `.env` in the project root with:

```
OPENAI_API_KEY=sk-...
```

2. Install dependencies (preferably inside a virtualenv):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open a browser on your Raspberry Pi and visit `http://localhost:5000` or access it from another device using the Pi's IP address.

Notes
- The backend expects OpenAI-compatible Chat Completions. Change the endpoint/payload if using a different API provider.
- When you have a physical LCD, you can run the same UI in a browser or implement a native display renderer that shows the HTML canvas.
# 🤖 AI Companion Robot

An interactive AI companion robot with animated eyes and ChatGPT integration. Perfect for Raspberry Pi with monitor display!

## Features

✨ **Animated Robot Face**
- Responsive eyes that blink and look around
- Expressive mouth that changes with emotions
- Smooth animations that work on all screen sizes
- Idle head bobbing animation

🧠 **AI Integration**
- ChatGPT API integration for intelligent responses
- Emotion detection based on responses
- Real-time chat interface

📱 **Fully Responsive**
- Works on all screen sizes (desktop, tablet, mobile)
- Optimized for Raspberry Pi with monitor
- Beautiful gradient UI

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- OpenAI API key (ChatGPT)

### Setup Steps

1. **Clone or navigate to project directory**
   ```bash
   cd /home/raspi/Desktop/LetLet_ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Open `.env` file
   - Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   - Local: `http://localhost:5000`
   - Remote (Raspberry Pi): `http://raspi_ip_address:5000`

## Project Structure

```
LetLet_ai/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── .env                   # API configuration
├── templates/
│   └── index.html        # Main HTML
└── static/
    ├── style.css         # Responsive styling
    └── script.js         # Frontend logic
```

## How It Works

1. **User Input**: Type a message in the chat box
2. **AI Processing**: Message is sent to ChatGPT via OpenAI API
3. **Emotion Detection**: Response is analyzed for emotion keywords
4. **Robot Response**: 
   - Robot's mouth changes expression
   - Eyes animate based on emotion
   - Status light indicates thinking/ready state
   - Message displayed in chat

## Emotions

The robot recognizes:
- 😊 **Happy** - Smiling mouth
- 😢 **Sad** - Sad mouth, crying eyes
- 😕 **Confused** - Surprised look
- 😐 **Neutral** - Straight line mouth

## Customization

### Change Robot Colors
Edit `static/style.css`:
```css
.robot-head {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

### Adjust Eye Speed
In `static/style.css`, modify animation duration:
```css
@keyframes lookAround {
    /* Change 4s to your desired speed */
    animation: lookAround 4s ease-in-out infinite;
}
```

### Modify AI Personality
In `app.py`, update the system message:
```python
{"role": "system", "content": "Your custom personality here..."}
```

## Running on Raspberry Pi

1. SSH into your Raspberry Pi
2. Follow installation steps above
3. Run: `python app.py`
4. On any device on the network, visit: `http://raspi_ip:5000`

## Troubleshooting

**Issue**: API key error
- Solution: Check `.env` file has correct API key

**Issue**: Port already in use
- Solution: Change port in `app.py`: `app.run(port=5001)`

**Issue**: CORS errors
- Solution: Flask-CORS is already configured

**Issue**: Slow responses
- Solution: Check internet connection and API rate limits

## Future Enhancements

- Voice input/output
- Multiple personality modes
- Gesture recognition
- Extended emoji expressions
- Recording conversations
- Custom voice synthesis

## License

MIT License - Feel free to modify and use!

## Support

For issues or questions, check the code comments or modify as needed.

Happy chatting with your AI companion! 🤖✨
