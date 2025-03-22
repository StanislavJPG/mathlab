from django.db import models
from django.utils.translation import gettext_lazy as _

from django_lifecycle import LifecycleModel, hook, AFTER_CREATE
from dynamic_filenames import FilePattern

from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


upload_to_pattern_draft = FilePattern(
    filename_pattern='{app_label:.25}/{instance.theorist.full_name_slug}/drafts/{uuid:s}{ext}'
)


class TheoristDrafts(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    label = models.CharField(max_length=95, null=True)
    draft = models.ImageField(max_length=300, upload_to=upload_to_pattern_draft)
    description = models.TextField(null=True, blank=True)

    is_public_available = models.BooleanField(default=False)

    theorist = models.ForeignKey('theorist.Theorist', on_delete=models.CASCADE, related_name='drafts')

    def __str__(self):
        return f'{self.label} | {self.__class__.__name__} | id - {self.id}'

    @hook(AFTER_CREATE)
    def after_create(self):
        if not self.label:
            self.set_default_label()

    def set_default_label(self):
        drafts_count = TheoristDrafts.objects.filter(therorist=self.theorist).count()
        self.label = _('Draft #%s') % drafts_count
        self.save(update_fields=['label'])
