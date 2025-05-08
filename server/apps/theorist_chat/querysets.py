from django.db import models
from django.db.models import Case, When, Value, IntegerField, F


class TheoristChatRoomQuerySet(models.QuerySet):
    def order_by_last_sms_sent_relevancy(self):
        return self.order_by(
            Case(
                When(last_sms_sent_at__isnull=True, then=Value(0)), default=Value(1), output_field=IntegerField()
            ).desc(),
            F('last_sms_sent_at').desc(),
        )


class TheoristMessageQueryset(models.QuerySet):
    def filter_by_is_safe_deleted(self):
        return self.filter(is_safe_deleted=True)
