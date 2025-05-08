from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_lifecycle import LifecycleModel, hook, AFTER_CREATE
from dynamic_filenames import FilePattern
from easy_thumbnails.files import get_thumbnailer

from server.apps.theorist_drafts.querysets import TheoristDraftsConfigurationQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


upload_to_pattern_draft = FilePattern(
    filename_pattern='{app_label:.25}/{instance.theorist.full_name_slug}/drafts/{uuid:s}{ext}'
)


class TheoristDrafts(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    label = models.CharField(max_length=95, null=True, blank=True)
    draft = models.ImageField(max_length=300, upload_to=upload_to_pattern_draft)
    description = models.TextField(null=True, blank=True, max_length=255)

    is_public_available = models.BooleanField(default=False)

    theorist = models.ForeignKey('theorist.Theorist', on_delete=models.CASCADE, related_name='drafts')

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Theorist Drafts'
        verbose_name = 'Theorist Draft'

    def __str__(self):
        return f'{self.label} | {self.__class__.__name__} | id - {self.id}'

    def get_absolute_url(self):
        return reverse('mathlab:drafts:base-drafts')

    def get_draft_url(self, size: list = None):
        thumbnailer = get_thumbnailer(self.draft)
        thumb = thumbnailer.get_thumbnail(
            {
                'size': (2105, 2000) if not size else size,
                'crop': 'smart',
            }
        )
        draft_url = thumb.url
        return draft_url

    @hook(AFTER_CREATE)
    def after_create(self):
        if not self.label:
            self.set_default_label()

    def set_default_label(self):
        drafts_count = TheoristDrafts.objects.filter(theorist=self.theorist).count()
        self.label = _('Draft #%s') % drafts_count
        self.save(update_fields=['label'])


class TheoristDraftsConfiguration(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    theorist = models.OneToOneField('theorist.Theorist', on_delete=models.CASCADE, related_name='drafts_configuration')
    is_public_available = models.BooleanField(default=True)

    objects = TheoristDraftsConfigurationQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Theorist Drafts Configurations'
        verbose_name = 'Theorist Draft Configuration'

    def __str__(self):
        return f'{self.theorist.full_name} | {self.__class__.__name__} | id - {self.id}'

    def get_share_url(self):
        return reverse('mathlab:drafts:base-drafts') + f'?search_draft={self.uuid}'
