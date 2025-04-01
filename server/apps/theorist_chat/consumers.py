import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TheoristChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_uuid = self.scope['url_route']['kwargs']['room_uuid']
        async_to_sync(self.channel_layer.group_add)(self.room_group_uuid, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_uuid, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(self.room_group_uuid, {'type': 'chat.message', 'message': message})

    def _context(self, event):
        user = self.scope['user']
        context = {'message': event['message'], 'msg_avatar_url': user.theorist.get_current_avatar_url()}
        return context

    def chat_message(self, event):
        context = self._context(event)

        # Send message to WebSocket
        self.send(text_data=json.dumps(context))
