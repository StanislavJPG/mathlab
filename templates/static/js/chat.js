const chatSocket = new WebSocket('ws://' + '127.0.0.1:8000' + '/ws/chat/');
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data['message'];
    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    const messageContainer = document.getElementsByClassName('messageContainer')[0]; // Get the first element with class 'messageContainer'
    messageContainer.appendChild(messageElement);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

function sendMessage(username) {
    const messageInput = document.getElementById("messageInput");
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': `${username} написав: ${message}`
    }));
}