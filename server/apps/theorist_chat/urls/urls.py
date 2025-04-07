from django.urls import path

from server.apps.theorist_chat.logic.chat import ChatView, MailBoxListView, ChatMessagesListView, HXMailBoxView
from server.apps.theorist_chat.logic.mailbox_management import MailBoxDeleteView, MailBoxCreateView
from server.apps.theorist_chat.logic.sharing import MessageDraftShareView

app_name = 'theorist_chat'

urlpatterns = [
    # Base views
    path('mailbox/', ChatView.as_view(), name='chat-base-page'),
    path('hx/mailbox/list/', MailBoxListView.as_view(), name='hx-mailbox-list'),
    path('hx/chat/<uuid:room_uuid>/', ChatMessagesListView.as_view(), name='hx-chat-list'),
    path('hx/mailbox/<uuid:room_uuid>/', HXMailBoxView.as_view(), name='hx-mailbox'),
    # Management mailbox views
    path('mailbox/create/', MailBoxCreateView.as_view(), name='mailbox-create'),
    path('mailbox/<uuid:uuid>/delete/', MailBoxDeleteView.as_view(), name='mailbox-delete'),
    # Share messages views
    path(
        'chat/drafts/<uuid:instance_uuid>/share/',
        MessageDraftShareView.as_view(),
        name='share-drafts-via-chat',
    ),
]
