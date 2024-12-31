const API_URL = 'http://127.0.0.1:5000/chat';

function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const sendButton = document.getElementById('sendButton');
    const loadingIndicator = document.getElementById('loading');

    if (!userInput) return;

    const messageContainer = document.getElementById('messages');
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user');
    userMessage.textContent = userInput;
    messageContainer.appendChild(userMessage);

    // Display loading indicator
    loadingIndicator.classList.add('show');
    sendButton.disabled = true;

    fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('div');
        botMessage.classList.add('message');
        botMessage.textContent = data.reply;
        messageContainer.appendChild(botMessage);
        document.getElementById('userInput').value = '';
        messageContainer.scrollTop = messageContainer.scrollHeight;

        // Hide loading indicator
        loadingIndicator.classList.remove('show');
        sendButton.disabled = false;
    })
    .catch(error => {
        console.error('Error:', error);

        // Hide loading indicator
        loadingIndicator.classList.remove('show');
        sendButton.disabled = false;
    });
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
