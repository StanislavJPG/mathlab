import json

import bleach
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import dateformat

from server.apps.theorist_chat.forms import TheoristMessageForm


class TheoristChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_uuid = self.scope['url_route']['kwargs']['room_uuid']
        async_to_sync(self.channel_layer.group_add)(self.room_group_uuid, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_uuid, self.channel_name)

    def _get_context(self):
        user = self.scope['user']
        response = {
            'theorist_avatar_url': user.theorist.get_current_avatar_url(),
            'theorist_uuid': str(user.theorist.uuid),
            'theorist_full_name': user.theorist.full_name,
            'theorist_created_at': dateformat.format(user.theorist.created_at, 'd E Y р. H:i'),
        }
        return response

    def _save_data_to_db(self, **kwargs):
        msg = kwargs.get('message', '')
        user = self.scope['user']
        kwargs.update({'room_uuid': self.room_group_uuid})
        sanitized_form = TheoristMessageForm(data={'message': msg})
        if sanitized_form.is_valid():
            sanitized_form.save(theorist=user.theorist, **kwargs)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = bleach.clean(text_data_json['message'])
        response = self._get_context()
        response.update({'message': message})
        self._save_data_to_db(**response)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_uuid, {'type': 'chat_message', 'message': response}
        )

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event['message']))
