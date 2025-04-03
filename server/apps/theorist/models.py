from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_SAVE

from slugify import slugify

from server.apps.theorist_chat.models import TheoristChatGroupConfiguration
from server.apps.theorist_drafts.models import TheoristDraftsConfiguration
from server.common.mixins.models import (
    UUIDModelMixin,
    TimeStampedModelMixin,
    AvatarModelMixin,
    RankSystemModelMixin,
)


class Theorist(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel, RankSystemModelMixin, AvatarModelMixin):
    """Model for business logic of web-site user. User model uses only for auth purposes."""

    # personal info
    full_name = models.CharField(max_length=150)
    country = CountryField(blank_label=_('Country'), null=True)
    about_me = models.TextField(_('About me'), blank=True)

    full_name_slug = models.SlugField(max_length=255, null=True, blank=True)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)

    # contact info urls
    social_media_url = models.URLField(max_length=225, null=True, blank=True)
    website_url = models.URLField(max_length=225, null=True, blank=True)

    # forum statistics data
    total_posts = models.PositiveSmallIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)

    is_onboarded = models.BooleanField(default=False)
    onboarding_date = models.DateTimeField(null=True)

    last_activity = models.DateTimeField(auto_now=True)  # TODO: fix or remove

    class Meta:
        verbose_name = 'theorist'
        verbose_name_plural = 'theorists'

    def __str__(self):
        return f'{self.full_name} | {self.__class__.__name__} | id - {self.id}'

    def get_absolute_url(self):
        return reverse(
            'forum:theorist_profile:base-page',
            kwargs={'pk': self.pk, 'full_name_slug': self.full_name_slug},
        )

    def get_boringavatars_url(self):
        return reverse(
            'forum:theorist_profile:theorist-avatar',
            kwargs={'uuid': self.uuid},
        )

    @hook(AFTER_CREATE)
    def create_initial_data(self):
        TheoristProfileSettings.objects.create(theorist=self)
        TheoristDraftsConfiguration.objects.create(theorist=self)
        TheoristChatGroupConfiguration.objects.create(theorist=self)

    @hook(AFTER_SAVE)
    def after_save(self):
        self.full_name_slug = slugify(self.full_name)
        self.save(update_fields=['full_name_slug'], skip_hooks=True)

    @property
    def convenient_last_activity(self):
        last_activity_label = _('Last activity %s ago') % timesince(self.last_activity)
        return last_activity_label

    def apply_default_onboarding_data(self):
        # use .save() outside explicitly
        self.is_onboarded = True
        self.onboarding_date = timezone.now()

    def deactivate(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])


class TheoristProfileSettings(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    theorist = models.OneToOneField('theorist.Theorist', on_delete=models.CASCADE, related_name='settings')

    is_profile_only_for_authenticated = models.BooleanField(default=False)  # is only auth people can visit my profile

    is_show_about_me = models.BooleanField(default=True)
    is_show_last_activities = models.BooleanField(default=True)
    is_able_to_get_messages = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'theorist profile setting'
        verbose_name_plural = 'theorist profile settings'

    def __str__(self):
        return f'{self.theorist.full_name} | {self.__class__.__name__} | id - {self.id}'

    def get_absolute_url(self):
        return reverse(
            'forum:theorist_profile:settings:theorist-profile-settings',
        )

    @property
    def is_about_me_is_available(self) -> bool:
        return self.is_show_about_me and self.theorist.about_me
