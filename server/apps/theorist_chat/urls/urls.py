from django.urls import path

from server.apps.theorist_chat.logic.chat import ChatView, MailBoxListView, ChatMessagesListView, HXMailBoxView
from server.apps.theorist_chat.logic.mailbox_management import (
    MailBoxDeleteView,
    MailBoxCreateView,
    MailBoxCreateFromProfile,
)
from server.apps.theorist_chat.logic.message_management import (
    InvalidChatMessageCreateView,
    ChatMessageSafeDeleteView,
    ChatMessageRestoreAfterSafeDeleteView,
)
from server.apps.theorist_chat.logic.sharing import MessageDraftShareView, MessageCommentShareView, MessagePostShareView

app_name = 'theorist_chat'

urlpatterns = [
    # Base views
    path('mailbox/', ChatView.as_view(), name='chat-base-page'),
    path('hx/mailbox/list/', MailBoxListView.as_view(), name='hx-mailbox-list'),
    path('hx/chat/<uuid:room_uuid>/', ChatMessagesListView.as_view(), name='hx-chat-list'),
    path('hx/mailbox/<uuid:room_uuid>/', HXMailBoxView.as_view(), name='hx-mailbox'),
    # Management mailbox views
    path('mailbox/create/', MailBoxCreateView.as_view(), name='mailbox-create'),
    path(
        'mailbox/<uuid:theorist_uuid>/from-profile-create/',
        MailBoxCreateFromProfile.as_view(),
        name='mailbox-create-from-profile',
    ),
    path('mailbox/<uuid:uuid>/delete/', MailBoxDeleteView.as_view(), name='mailbox-delete'),
    # Management messages views
    path('messages/<uuid:uuid>/safe-delete/', ChatMessageSafeDeleteView.as_view(), name='chat-message-safe-delete'),
    path('messages/<uuid:uuid>/restore/', ChatMessageRestoreAfterSafeDeleteView.as_view(), name='chat-message-restore'),
    path('messages/fail-create/', InvalidChatMessageCreateView.as_view(), name='invalid-chat-message-create'),
    # Share messages views
    path(
        'chat/drafts/<uuid:instance_uuid>/share/',
        MessageDraftShareView.as_view(),
        name='share-drafts-via-chat',
    ),
    path(
        'chat/comments/<uuid:instance_uuid>/share/',
        MessageCommentShareView.as_view(),
        name='share-comments-via-chat',
    ),
    path(
        'chat/posts/<uuid:instance_uuid>/share/',
        MessagePostShareView.as_view(),
        name='share-posts-via-chat',
    ),
]
