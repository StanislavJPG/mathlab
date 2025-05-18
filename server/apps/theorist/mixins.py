from django.contrib.contenttypes.models import ContentType

from server.apps.theorist_notifications.signals import notify


class NotificationFriendshipMixin:
    notification_display_name = None

    def get_notification_display_name(self):
        if self.notification_display_name is None:
            raise NotImplementedError('`notification_display_name` is not defined')
        return self.notification_display_name

    def send_notify(self, object=None):
        self.object = self.get_object() if not object else object
        recipient = self.object.requester if self.request.theorist == self.object.receiver else self.object.receiver
        display_name = self.get_notification_display_name()
        notify.send(
            sender=self.request.theorist,
            recipient=recipient.user,
            actor_content_type=ContentType.objects.get_for_model(recipient),
            target=self.object,
            action_object=self.object,
            public=False,
            action_url=self.request.theorist.get_absolute_url(),
            target_display_name=display_name,
        )
