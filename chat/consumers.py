import json
from channels.generic.websocket import AsyncWebsocketConsumer


class Chat(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        ...

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = f'{text_data_json["message"]}'

        await self.send(text_data=json.dumps(
            {'message': message}
        ))
