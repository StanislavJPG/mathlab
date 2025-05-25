from django.db import models
from django.utils.html import format_html
from notifications.base.models import AbstractNotification

from server.common.mixins.models import UUIDModelMixin


class TheoristNotification(UUIDModelMixin, AbstractNotification):
    action_url = models.URLField(null=True, blank=True)

    actor_display_name = models.CharField(max_length=255, null=True)
    target_display_name = models.CharField(max_length=255, null=True)

    theorist = models.ForeignKey('theorist.Theorist', on_delete=models.CASCADE, related_name='notifications', null=True)

    class Meta(AbstractNotification.Meta):
        abstract = False

    def extend_notification(
        self,
        request_theorist=None,
        action_url=None,
        actor_display_name=None,
        target_display_name=None,
    ):
        _props = self._important_props_create(request_theorist or self.recipient.theorist)
        update_fields = [*_props]
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

    def _important_props_create(self, theorist):
        """create important props and return tuple of changed fields"""
        self.theorist = theorist
        return ('theorist',)

    def safe_delete(self):
        self.deleted = True
        self.unread = False
        self.save(update_fields=['deleted', 'unread'])

    @property
    def notification_label_as_html_tag(self):
        return format_html(f'<strong>{self.actor_display_name}</strong> {self.verb} {self.target_display_name}')
