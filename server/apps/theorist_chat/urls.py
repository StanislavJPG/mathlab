from django.urls import path

from server.apps.theorist_chat.logic.chat import ChatView, MailBoxListView, ChatMessagesListView, HXMailBoxView
from server.apps.theorist_chat.logic.mailbox_management import MailBoxDeleteView

app_name = 'theorist_chat'

urlpatterns = [
    # Base views
    path('mailbox/', ChatView.as_view(), name='chat-base-page'),
    path('hx/mailbox/list/', MailBoxListView.as_view(), name='hx-mailbox-list'),
    path('hx/chat/<uuid:room_uuid>/', ChatMessagesListView.as_view(), name='hx-chat-list'),
    path('hx/mailbox/', HXMailBoxView.as_view(), name='hx-mailbox'),
    # Management views
    path('mailbox/<uuid:uuid>/delete/', MailBoxDeleteView.as_view(), name='mailbox-delete'),
]
