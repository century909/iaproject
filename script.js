document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    const API_URL = 'http://127.0.0.1:8000/chat';
    const characterPrompt = "You are a cheerful pirate captain named Red. You love to say 'Ahoy!' and talk about treasure. Keep your responses brief and in character.";
    let conversationHistory = [];

    /**
     * Adds a message to the chat window.
     * @param {string} message The message content.
     * @param {string} sender 'user' or 'ai'.
     */
    function addMessageToWindow(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'ai-message');

        // Sanitize text to prevent HTML injection
        messageDiv.textContent = message;

        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the latest message
    }

    /**
     * Sends the user's message to the backend API and displays the response.
     */
    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        addMessageToWindow(userMessage, 'user');

        const currentHistory = [...conversationHistory];
        conversationHistory.push({ role: 'user', content: userMessage });

        userInput.value = ''; // Clear input field immediately
        userInput.focus();

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    character_prompt: characterPrompt,
                    user_message: userMessage,
                    conversation_history: currentHistory
                })
            });

            if (!response.ok) {
                throw new Error(`API request failed with status ${response.status}`);
            }

            const data = await response.json();
            const aiMessage = data.ai_message;

            addMessageToWindow(aiMessage, 'ai');
            conversationHistory.push({ role: 'assistant', content: aiMessage });

        } catch (error) {
            console.error('Error fetching AI response:', error);
            addMessageToWindow('Sorry, me parrot seems to have flown off with the response. Try again!', 'ai');
        }
    }

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Initial greeting from the AI
    const initialGreeting = "Ahoy there, matey! I be Captain Red. What be on yer mind?";
    addMessageToWindow(initialGreeting, 'ai');
    conversationHistory.push({ role: 'assistant', content: initialGreeting });
});
