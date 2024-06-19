from django.urls import path

from chat.views import ChatView, ChatListView

urlpatterns = [
    path('chat/communication/<int:receiver>/<str:username>', ChatView.as_view(), name='ws-chat'),
    path('chat/list/', ChatListView.as_view(), name='chat-list')
]
