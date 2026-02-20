#!/bin/bash

# AI Companion Robot - Quick Start Script

echo "🤖 AI Companion Robot Startup"
echo "=============================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Start the Flask app
echo "Starting AI Robot Server..."
echo "=============================="
echo "🌐 Server running at: http://localhost:5000"
echo "📱 Remote access: http://$(hostname -I | awk '{print $1}'):5000"
echo "=============================="
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
