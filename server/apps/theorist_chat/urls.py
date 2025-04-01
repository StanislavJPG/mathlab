from django.urls import path

from server.apps.theorist_chat.logic.chat import ChatView

app_name = 'theorist_chat'

urlpatterns = [
    path('mailbox/<uuid:uuid>/', ChatView.as_view(), name='chat-base-page'),
]
