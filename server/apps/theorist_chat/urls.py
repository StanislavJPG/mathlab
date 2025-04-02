from django.urls import path

from server.apps.theorist_chat.logic.chat import ChatView, MailBoxListView, ChatMessagesListView

app_name = 'theorist_chat'

urlpatterns = [
    path('mailbox/', ChatView.as_view(), name='chat-base-page'),
    path('hx/mailbox/', MailBoxListView.as_view(), name='hx-mailbox-list'),
    path('hx/chat/<uuid:room_uuid>/', ChatMessagesListView.as_view(), name='hx-chat-list'),
]
