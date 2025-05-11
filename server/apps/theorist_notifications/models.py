from django.db import models
from notifications.base.models import AbstractNotification


class TheoristNotification(AbstractNotification):
    action_url = models.URLField(null=True, blank=True)

    actor_display_name = models.CharField(max_length=255, null=True)
    target_display_name = models.CharField(max_length=255, null=True)

    class Meta(AbstractNotification.Meta):
        abstract = False

    def extend_notification(
        self,
        action_url=None,
        actor_display_name=None,
        target_display_name=None,
    ):
        update_fields = []
        if action_url:
            self.action_url = action_url
            update_fields.append('action_url')
        if actor_display_name or hasattr(self.actor, 'full_name'):
            self.actor_display_name = actor_display_name or self.actor.full_name
            update_fields.append('actor_display_name')
        if target_display_name:
            self.target_display_name = target_display_name
            update_fields.append('target_display_name')

        self.save(update_fields=update_fields)
