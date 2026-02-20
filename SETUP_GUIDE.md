# 🤖 AI Robot Setup & Usage Guide

## Quick Start (Fastest Way)

### Run on Raspberry Pi (Terminal)
```bash
cd /home/raspi/Desktop/LetLet_ai
./run.sh
```

That's it! The script will:
- ✅ Create virtual environment (if needed)
- ✅ Activate it
- ✅ Install dependencies
- ✅ Start the server

### Access the Robot
- **Local (on Raspi)**: Open browser → `http://localhost:5000`
- **From another device**: `http://raspi_ip_address:5000`
  - Find IP: Run `hostname -I` on Raspberry Pi

---

## Manual Setup (Step by Step)

### 1. Navigate to Project
```bash
cd /home/raspi/Desktop/LetLet_ai
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment
```bash
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure API Key
- Open `.env` file in text editor
- Verify your OpenAI API key is there:
```
OPENAI_API_KEY=sk-proj-...your_key...
```

### 6. Start Server
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

## Using Your AI Robot

### What You Can Do:
1. **Ask Questions**: "What is the capital of France?"
2. **Have Conversations**: "Tell me a joke"
3. **Get Help**: "How do I make pizza?"
4. **Discuss Topics**: "Explain machine learning"

### Robot Expressions:
The robot shows emotions based on responses:
- 😊 **Happy** - Positive responses
- 😢 **Sad** - Negative or sad responses
- 😕 **Confused** - Unclear or questioning responses
- 😐 **Neutral** - Regular responses

### Eye Animations:
- Eyes **blink** continuously
- Eyes **look around** idly
- Head **bobs** gently
- Hover over head to **stop** bobbing

---

## Project Files Explained

```
LetLet_ai/
├── app.py                 # Flask backend - handles API calls
├── requirements.txt       # Python packages needed
├── .env                   # API key (KEEP SECRET!)
├── run.sh                 # Quick start script
├── README.md              # Project documentation
├── templates/
│   └── index.html        # Main page structure
└── static/
    ├── style.css         # All styling & animations
    └── script.js         # Chat & animation logic
```

---

## Customization Ideas

### 1. Change Robot Colors
**File**: `static/style.css`

Find `.robot-head` and change:
```css
.robot-head {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

Try: `#FF6B6B`, `#4ECDC4`, `#FFE66D`

### 2. Adjust Robot Personality
**File**: `app.py`

Find this line and customize:
```python
{"role": "system", "content": "You are a friendly AI companion robot..."}
```

Examples:
- "You are a pirate robot, speak like a pirate"
- "You are a scientific robot, give detailed explanations"
- "You are a silly robot that makes jokes"

### 3. Change Animation Speed
**File**: `static/style.css`

Find `@keyframes` sections and change time values:
- `3s` = 3 seconds
- `4s` = 4 seconds

### 4. Add Background Music
**File**: `templates/index.html`

Add to `<head>` section:
```html
<audio autoplay loop>
    <source src="path/to/music.mp3" type="audio/mpeg">
</audio>
```

---

## Troubleshooting

### ❌ "API Key Error"
- Check `.env` file exists in project folder
- Verify API key is correct (no extra spaces)
- Make sure it starts with `sk-proj-`

### ❌ "Port 5000 Already in Use"
- Open `app.py`
- Change `port=5000` to `port=5001` (or any free port)
- Restart server

### ❌ "Module not found" Error
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt` again

### ❌ "Connection Refused" (can't access from other device)
- Check Raspberry Pi IP: `hostname -I`
- Make sure firewall allows port 5000
- Try: `http://raspi_ip:5000` instead of localhost

### ❌ "OpenAI API Error"
- Check internet connection
- Verify API key has credits
- Check OpenAI account status
- Check rate limits aren't exceeded

### ❌ Robot doesn't respond
- Look at browser console (F12 → Console)
- Check terminal for error messages
- Restart server
- Try simpler question first

---

## Performance Tips

### For Raspberry Pi 4:
- Works great! ✅
- Animations smooth
- No lag

### For Raspberry Pi 3:
- May need lower animation complexity
- Consider disabling some animations if slow

### To Improve Speed:
1. Close other applications
2. Reduce browser tabs
3. Use latest Chromium browser
4. Lower animation frame rate

---

## Advanced: Run on Startup

### Auto-start on Raspberry Pi Boot:

1. Edit crontab:
```bash
crontab -e
```

2. Add this line at the end:
```
@reboot cd /home/raspi/Desktop/LetLet_ai && ./run.sh &
```

3. Save (Ctrl+O, Enter, Ctrl+X)

Now server starts automatically on boot!

---

## Advanced: Use Different AI Model

### Switch to GPT-4 (if you have access):

**File**: `app.py`

Change:
```python
model="gpt-3.5-turbo"
```

To:
```python
model="gpt-4"
```

Note: GPT-4 costs more per request

---

## Tips & Tricks

1. **Multi-device**: Open in multiple browsers simultaneously
2. **Fullscreen**: Press F11 for fullscreen mode
3. **Mobile friendly**: Works great on tablets/phones too
4. **Adjustable text size**: Zoom in/out with Ctrl/Cmd + scroll

---

## Next Steps

1. Try different personalities
2. Customize colors to match your robot's physical design
3. Add voice input (future enhancement)
4. Create different modes (serious, funny, educational)
5. Record conversations
6. Build physical interface with buttons

---

## Need Help?

- Check the README.md for more info
- Look at code comments in files
- Test with simple questions first
- Check terminal output for errors

---

**Enjoy your AI companion robot! 🤖✨**
