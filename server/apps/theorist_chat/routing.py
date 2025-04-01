from django.urls import re_path

from server.apps.theorist_chat.consumers import TheoristChatConsumer

websocket_urlpatterns = [
    re_path('chat/<group_uuid:uuid>/', TheoristChatConsumer.as_asgi()),
]
