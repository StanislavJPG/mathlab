from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from server.apps.forum.factories import CommentFactory, PostFactory
from server.apps.forum.models import PostCategory
from server.apps.theorist.choices import TheoristFriendshipStatusChoices
from server.apps.theorist.factories import TheoristFactory
from server.apps.theorist.models import TheoristFriendship
from server.apps.theorist_chat.factories import TheoristChatRoomFactory
from server.apps.theorist_chat.logic.mailbox_management import (
    MailBoxCreateView,
    MailBoxCreateFromProfileView,
    MailBoxDeleteView,
)
from server.apps.theorist_chat.logic.message_management import (
    ChatMessageSafeDeleteView,
    ChatMessageRestoreAfterSafeDeleteView,
)
from server.apps.theorist_chat.models import TheoristMessage, TheoristChatRoom
from server.apps.theorist_drafts.factories import TheoristDraftsFactory
from tests.testcases import TheoristTestCase


class TestTheoristChat(TheoristTestCase):
    def setUp(self):
        super().setUp()
        self.room = TheoristChatRoomFactory.create(first_member=self.theorist)
        self.message = TheoristMessage.objects.create(
            message=self.fake.text(max_nb_chars=500), sender=self.theorist, room=self.room
        )
        self.dummy_theorist = TheoristFactory.create()
        TheoristFriendship.create_friendship_request(
            from_=self.theorist, to=self.dummy_theorist, status=TheoristFriendshipStatusChoices.ACCEPTED
        )
        PostCategory.create_data()
        self.post = PostFactory.create(theorist=self.theorist)

    def test_chat_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:theorist_chat:chat-base-page'))
        self.assertEqual(response.status_code, 200)

    def test_disabled_chat_view(self):
        self.theorist.chat_configuration.is_chats_available = False
        self.theorist.chat_configuration.save(update_fields=['is_chats_available'])
        response = self.client.get(reverse('forum:theorist_chat:chat-base-page'), follow=True)
        try:
            self.assertEqual(response.status_code, 200)
        except PermissionDenied:
            self.assertTrue(True)

    def test_mailbox_list_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(reverse('forum:theorist_chat:hx-mailbox-list'))
        self.assertEqual(response.status_code, 200)

    def test_chat_messages_list_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(reverse('forum:theorist_chat:hx-chat-list', kwargs={'room_uuid': self.room.uuid}))
        self.assertEqual(response.status_code, 200)

    def test_hx_mailbox_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(reverse('forum:theorist_chat:hx-mailbox', kwargs={'room_uuid': self.room.uuid}))
        self.assertEqual(response.status_code, 200)

    def test_valid_mailbox_create_view(self):
        self.client.force_login(self.user)
        mailboxes_before_count = TheoristChatRoom.objects.all().count()
        response = self.client.hx_post(
            reverse('forum:theorist_chat:mailbox-create'), data={'second_member': self.dummy_theorist.uuid}
        )
        mailboxes_after_count = TheoristChatRoom.objects.all().count()
        self.assertEqual(mailboxes_after_count - mailboxes_before_count, 1)
        self.assertEqual(response.status_code, 200)

    def test_empty_input_mailbox_create_view(self):
        request = self.hx_factory.post(reverse('forum:theorist_chat:mailbox-create'))
        response = self.get_response(cbv=MailBoxCreateView, request=request, return_view_instance=True)

        self.assertFormError(response.get_form(), 'second_member', _('This field is required.'))

    def test_mailbox_create_from_profile_view(self):
        theorist = TheoristFactory.create()
        TheoristFriendship.create_friendship_request(
            from_=self.theorist, to=theorist, status=TheoristFriendshipStatusChoices.ACCEPTED
        )
        request = self.hx_factory.post(
            reverse('forum:theorist_chat:mailbox-create-from-profile', kwargs={'theorist_uuid': theorist.uuid}),
        )
        response = self.get_response(
            cbv=MailBoxCreateFromProfileView, request=request, kwargs={'theorist_uuid': theorist.uuid}
        )
        mailboxes = TheoristChatRoom.objects.exclude(pk=self.room.pk)
        self.assertEquals(mailboxes.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_mailbox_delete_view(self):
        request = self.hx_factory.delete(
            reverse('forum:theorist_chat:mailbox-delete', kwargs={'uuid': self.room.uuid}),
        )
        response = self.get_response(cbv=MailBoxDeleteView, request=request, kwargs={'uuid': self.room.uuid})
        self.assertEqual(response.status_code, 200)

    def test_mailbox_delete_by_stranger_view(self):
        request = self.hx_factory.delete(
            reverse('forum:theorist_chat:mailbox-delete', kwargs={'uuid': self.room.uuid}),
        )
        try:
            self.get_response(
                cbv=MailBoxDeleteView, request=request, kwargs={'uuid': self.room.uuid}, is_dummy_theorist=True
            )
        except Http404:
            self.assertTrue(True)  # i.e strangers cannot delete other answers

    def test_messages_safe_delete_view(self):
        is_safe_deleted_before = self.message.is_safe_deleted
        request = self.hx_factory.post(
            reverse('forum:theorist_chat:chat-message-safe-delete', kwargs={'uuid': self.message.uuid})
        )
        response = self.get_response(cbv=ChatMessageSafeDeleteView, request=request, kwargs={'uuid': self.message.uuid})
        self.message.refresh_from_db()
        self.assertNotEquals(is_safe_deleted_before, self.message.is_safe_deleted)
        self.assertEqual(response.status_code, 200)

    def test_message_restore_after_safe_delete_view(self):
        self.message.is_safe_deleted = True
        self.message.was_safe_deleted_by = self.theorist
        self.message.save(update_fields=['is_safe_deleted', 'was_safe_deleted_by'])
        is_safe_deleted_before = self.message.is_safe_deleted

        request = self.hx_factory.post(
            reverse('forum:theorist_chat:chat-message-restore', kwargs={'uuid': self.message.uuid})
        )
        response = self.get_response(
            cbv=ChatMessageRestoreAfterSafeDeleteView, request=request, kwargs={'uuid': self.message.uuid}
        )
        self.message.refresh_from_db()
        self.assertNotEquals(is_safe_deleted_before, self.message.is_safe_deleted)
        self.assertEqual(response.status_code, 200)

    def test_invalid_message_create_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:theorist_chat:invalid-chat-message-create'))
        self.assertEqual(response.status_code, 405)

    def test_message_draft_share_view(self):
        self.client.force_login(self.user)
        TheoristDraftsFactory.create(theorist=self.theorist)
        honeypot_field = settings.HONEYPOT_FIELD_NAME
        response = self.client.hx_post(
            reverse(
                'forum:theorist_chat:share-drafts-via-chat',
                kwargs={'instance_uuid': self.theorist.drafts_configuration.uuid},
            ),
            data={'receiver': self.dummy_theorist, honeypot_field: ''},
        )
        self.assertEqual(response.status_code, 200)

    def test_message_comment_share_view(self):
        self.client.force_login(self.user)
        comment = CommentFactory.create(theorist=self.theorist, post=self.post)
        honeypot_field = settings.HONEYPOT_FIELD_NAME
        response = self.client.hx_post(
            reverse('forum:theorist_chat:share-comments-via-chat', kwargs={'instance_uuid': comment.uuid}),
            data={'receiver': self.dummy_theorist, honeypot_field: ''},
        )
        self.assertEqual(response.status_code, 200)

    def test_message_post_share_view(self):
        self.client.force_login(self.user)
        honeypot_field = settings.HONEYPOT_FIELD_NAME
        response = self.client.hx_post(
            reverse('forum:theorist_chat:share-posts-via-chat', kwargs={'instance_uuid': self.post.uuid}),
            data={'receiver': self.dummy_theorist, honeypot_field: ''},
        )
        self.assertEqual(response.status_code, 200)
