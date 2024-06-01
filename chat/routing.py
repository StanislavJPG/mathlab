from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from chat.consumers import Chat


application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    'websocket': URLRouter([
        path('ws/chat/', Chat.as_asgi()),
    ])
})
