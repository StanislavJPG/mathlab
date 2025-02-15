const chatSocket = new WebSocket('ws://' + '127.0.0.1:8000' + '/ws/chat/');
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = `${data['sender']} щойно написав: ${data['message']}`;
    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    const messageContainer = document.getElementsByClassName('messageContainer')[0];
    messageContainer.appendChild(messageElement);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

function sendMessage(sender_id, receiver_id) {
    const messageInput = document.getElementById("messageInput");
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
    }));
    messageInput.value = "";
}