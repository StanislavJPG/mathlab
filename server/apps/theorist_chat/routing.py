from django.urls import re_path

from server.apps.theorist_chat.consumers import TheoristChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_uuid>[0-9a-f-]{36})/$', TheoristChatConsumer.as_asgi()),
]
