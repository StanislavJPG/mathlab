import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from server.apps.chat.models import Message
from django.db.models import Q

from server.apps.users.models import CustomUser


class Chat(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code): ...

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        # check here
        message = (
            text_data_json['message'] if len(text_data_json['message']) <= 50 else None
        )
        sender_id = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']
        data = {'message': message}

        cached_data = cache.get(f'sender_id.{sender_id}: receiver_id.{receiver_id}')
        if not cached_data:
            cached_sender, cached_receiver = None, None
            async for user in CustomUser.objects.filter(
                Q(id=sender_id) | Q(id=receiver_id)
            ):
                if user.id == sender_id:
                    cached_sender = user
                else:
                    cached_receiver = user

            cache.set(
                f'sender_id.{sender_id}: receiver_id.{receiver_id}',
                {'sender': cached_sender, 'receiver': cached_receiver},
                60 * 10,
            )

            await Message.objects.acreate(
                sender=cached_sender, receiver=cached_receiver, message=message
            )

            data['sender'], data['receiver'] = (
                cached_sender.username,
                cached_receiver.username,
            )
        else:
            cached_sender = cached_data['sender'].username
            cached_receiver = cached_data['receiver'].username
            await Message.objects.acreate(
                sender=cached_data['sender'],
                receiver=cached_data['receiver'],
                message=message,
            )
            data['sender'], data['receiver'] = (cached_sender, cached_receiver)

        await self.send(text_data=json.dumps(data))
