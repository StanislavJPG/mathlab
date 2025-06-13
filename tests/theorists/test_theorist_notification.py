from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from server.apps.theorist.factories import TheoristFactory
from server.apps.theorist_notifications.logic.notifications import (
    HXReadNotificationsView,
    HXUnreadNotificationsListView,
    HXDeletedNotificationsListView,
)
from server.apps.theorist_notifications.logic.notifications_management import (
    NotificationMarkAllReadView,
    NotificationMarkAllDeletedView,
    NotificationMarkReadView,
    NotificationDeleteView,
)
from server.apps.theorist_notifications.models import TheoristNotification
from server.apps.theorist_notifications.signals import notify
from tests.testcases import TheoristTestCase


class TestTheoristNotification(TheoristTestCase):
    def setUp(self):
        super().setUp()
        sender = TheoristFactory.create()
        display_name = 'Test Display Name'
        notify.send(
            sender=sender,
            recipient=self.theorist.user,
            actor_content_type=ContentType.objects.get_for_model(self.theorist),
            target=self.theorist,
            action_object=self.theorist,
            public=False,
            action_url=self.theorist.get_absolute_url(),
            target_display_name=display_name,
        )
        self.notification = TheoristNotification.objects.first()

    def test_notification_template_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:theorist_notifications:all'))
        self.assertEqual(response.status_code, 200)

    def test_hx_read_notifications_list_view(self):
        request = self.hx_factory.get(reverse('forum:theorist_notifications:hx-notifications-read'))
        response = self.get_response(cbv=HXReadNotificationsView, request=request)
        self.assertEqual(response.status_code, 200)

    def test_hx_unread_notifications_list_view(self):
        request = self.hx_factory.get(reverse('forum:theorist_notifications:hx-notifications-unread'))
        response = self.get_response(cbv=HXUnreadNotificationsListView, request=request)
        self.assertEqual(response.status_code, 200)

    def test_hx_deleted_notifications_list_view(self):
        request = self.hx_factory.get(reverse('forum:theorist_notifications:hx-notifications-deleted'))
        response = self.get_response(cbv=HXDeletedNotificationsListView, request=request)
        self.assertEqual(response.status_code, 200)

    def test_notifications_mark_all_read_view(self):
        request = self.hx_factory.post(
            reverse('forum:theorist_notifications:mark-all-read'),
        )
        response = self.get_response(cbv=NotificationMarkAllReadView, request=request)
        self.assertEqual(response.status_code, 200)

    def test_notifications_mark_all_deleted_view(self):
        request = self.hx_factory.post(
            reverse('forum:theorist_notifications:mark-all-deleted'),
        )
        response = self.get_response(
            cbv=NotificationMarkAllDeletedView,
            request=request,
        )
        self.assertEqual(response.status_code, 200)

    def test_notification_mark_read_view(self):
        notification_before = self.notification.unread
        request = self.hx_factory.post(
            reverse('forum:theorist_notifications:mark-read', kwargs={'uuid': self.notification.uuid}),
        )
        response = self.get_response(
            cbv=NotificationMarkReadView, request=request, kwargs={'uuid': self.notification.uuid}
        )

        self.notification.refresh_from_db()
        self.assertNotEqual(notification_before, self.notification.unread)
        self.assertEqual(response.status_code, 200)

    def test_notification_safe_delete_view(self):
        notification_before = self.notification.deleted
        request = self.hx_factory.post(
            reverse('forum:theorist_notifications:safe-delete', kwargs={'uuid': self.notification.uuid}),
        )
        response = self.get_response(
            cbv=NotificationDeleteView, request=request, kwargs={'uuid': self.notification.uuid}
        )

        self.notification.refresh_from_db()
        self.assertNotEqual(notification_before, self.notification.deleted)
        self.assertEqual(response.status_code, 200)
