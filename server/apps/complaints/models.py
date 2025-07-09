from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel

from server.apps.complaints.querysets import ComplaintQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class Complaint(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    complaint_text = models.TextField(_('complaint text'))
    counter = models.PositiveSmallIntegerField(
        _('complaint counter'), default=0
    )  # number of complaints for specific object

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    processed = models.BooleanField(_('processed'), default=False)

    objects = ComplaintQuerySet.as_manager()

    class Meta:
        verbose_name = _('Complaint')
        verbose_name_plural = _('Complaints')
        ordering = ('-created_at', '-counter')

    def __str__(self):
        return f'{self.content_object} | {self.__class__.__name__} | id - {self.id}'
