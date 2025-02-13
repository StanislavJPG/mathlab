import uuid
from django.db import models
from django.utils import timezone


class TimeStampModelMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class UUIDModelMixin(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True
