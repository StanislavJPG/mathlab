from django.db import models
from django.utils import timezone


class TimeStampModelMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
