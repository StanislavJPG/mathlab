from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE

from server.apps.complaints.choices import ComplaintCategoryChoices
from server.apps.complaints.querysets import ComplaintQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class Complaint(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    complaint_text = models.TextField(_('complaint text'), validators=[MinLengthValidator(35)])
    category = models.CharField(_('category'), choices=ComplaintCategoryChoices.choices, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    counter = models.PositiveSmallIntegerField(
        _('complaint counter'), default=0
    )  # number of complaints for specific object
    processed = models.BooleanField(_('processed'), default=False)

    objects = ComplaintQuerySet.as_manager()

    class Meta:
        verbose_name = _('Complaint')
        verbose_name_plural = _('Complaints')
        ordering = ('-created_at', '-counter')

    def __str__(self):
        return f'{self.content_object} | {self.__class__.__name__} | id - {self.id}'

    @hook(AFTER_CREATE)
    def after_create(self):
        complaints_count = Complaint.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
        ).count()
        self.counter = complaints_count
        self.save(update_fields=['counter'])
