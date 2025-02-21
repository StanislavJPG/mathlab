from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from server.apps.chat.consumers import Chat


application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter(
            [
                path('ws/chat/', Chat.as_asgi()),
            ]
        ),
    }
)
