// DOM Elements
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const messagesContainer = document.getElementById('messages');
const robotHead = document.querySelector('.robot-head');
const statusLight = document.querySelector('.status-light');
const mouthPath = document.querySelector('.mouth-path');
const eyes = document.querySelectorAll('.eye');

// Initialize
let isWaiting = false;
let currentEmotion = 'neutral';

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !isWaiting) {
        sendMessage();
    }
});

// Initialize mouth
setMouthExpression('neutral');

async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message || isWaiting) return;
    
    // Add user message to chat
    addUserMessage(message);
    userInput.value = '';
    
    // Set thinking state
    isWaiting = true;
    sendBtn.disabled = true;
    statusLight.classList.add('thinking');
    setMouthExpression('surprised');
    showTypingIndicator();
    
    try {
        // Send to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Get emotion from response
            const emotion = data.emotion || 'neutral';
            currentEmotion = emotion;
            
            // Update robot expression
            setMouthExpression(emotion);
            playEyeAnimation(emotion);
            
            // Add robot response
            addRobotMessage(data.response);
        } else {
            removeTypingIndicator();
            addRobotMessage('Sorry, something went wrong. Please try again.');
            setMouthExpression('sad');
        }
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addRobotMessage('Connection error. Please make sure the server is running.');
        setMouthExpression('sad');
    } finally {
        isWaiting = false;
        sendBtn.disabled = false;
        statusLight.classList.remove('thinking');
    }
}

function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-group';
    messageDiv.innerHTML = `<div class="user-message"><p>${escapeHtml(message)}</p></div>`;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addRobotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-group';
    messageDiv.innerHTML = `<div class="robot-message"><p>${escapeHtml(message)}</p></div>`;
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message-group typing-group';
    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    scrollToBottom();
}

function removeTypingIndicator() {
    const typingGroup = document.querySelector('.typing-group');
    if (typingGroup) {
        typingGroup.remove();
    }
}

function scrollToBottom() {
    const chatDisplay = document.querySelector('.chat-display');
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

function setMouthExpression(emotion) {
    mouthPath.classList.remove('happy', 'sad', 'surprised', 'neutral');
    
    switch (emotion) {
        case 'happy':
            mouthPath.classList.add('happy');
            break;
        case 'sad':
            mouthPath.classList.add('sad');
            break;
        case 'confused':
            mouthPath.classList.add('surprised');
            break;
        default:
            mouthPath.classList.add('neutral');
    }
}

function playEyeAnimation(emotion) {
    eyes.forEach(eye => {
        eye.style.animation = 'none';
        setTimeout(() => {
            switch (emotion) {
                case 'happy':
                    eye.style.animation = 'happyBlink 0.6s ease';
                    break;
                case 'sad':
                    eye.style.animation = 'sadLook 0.8s ease';
                    break;
                case 'confused':
                    eye.style.animation = 'confusedLook 0.8s ease';
                    break;
                default:
                    eye.style.animation = 'blinkLeft 3s ease-in-out infinite, lookAround 4s ease-in-out infinite';
            }
        }, 10);
    });
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes happyBlink {
        0%, 100% { height: 100px; }
        50% { height: 20px; }
    }
    
    @keyframes sadLook {
        0%, 100% { transform: translateY(-5px); }
        50% { transform: translateY(10px); }
    }
    
    @keyframes confusedLook {
        0%, 100% { transform: translateX(0) rotate(0deg); }
        25% { transform: translateX(-10px) rotate(-5deg); }
        75% { transform: translateX(10px) rotate(5deg); }
    }
`;
document.head.appendChild(style);

// Robot head idle animations
robotHead.addEventListener('mouseenter', () => {
    robotHead.style.animation = 'none';
});

robotHead.addEventListener('mouseleave', () => {
    robotHead.style.animation = 'headBob 3s ease-in-out infinite';
});
