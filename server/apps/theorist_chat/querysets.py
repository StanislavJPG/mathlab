from django.db import models
from django.db.models import Case, When, F, Max, DateTimeField


class TheoristChatRoomQuerySet(models.QuerySet):
    def order_by_last_sms_sent_relevancy(self):
        return self.annotate(
            # `last_sms_sent_at_max` gets the latest message time
            last_sms_sent_at_max=Max('last_sms_sent_at'),
            # `last_activity`: `last_sms_sent_at_max if last_sms_sent_at_max is not None else created_at`
            last_activity=Case(
                When(last_sms_sent_at_max__isnull=False, then=F('last_sms_sent_at_max')),
                default=F('created_at'),
                output_field=DateTimeField(),
            ),
        ).order_by('-last_activity')


class TheoristMessageQueryset(models.QuerySet):
    def filter_by_is_safe_deleted(self):
        return self.filter(is_safe_deleted=True)

    def filter_by_is_not_safe_deleted(self):
        return self.filter(is_safe_deleted=False)

    def filter_by_is_read(self):
        return self.filter(is_read=True)

    def filter_by_is_unread(self):
        return self.filter(is_read=False)

    def mark_messages_as_read(self):
        return self.update(is_read=True)
