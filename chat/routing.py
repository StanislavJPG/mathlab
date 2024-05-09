from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from chat.consumers import Chat


application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    # 'http': get_asgi_application(),
    'websocket': URLRouter([
        path('ws/chat/', Chat.as_asgi()),
    ])
})
