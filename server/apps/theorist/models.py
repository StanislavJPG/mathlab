from django.db import models
from django.urls import reverse

from django_lifecycle import LifecycleModel, hook, BEFORE_SAVE

from slugify import slugify

from server.apps.theorist.choices import TheoristRankChoices
from server.common.mixins.models import (
    UUIDModelMixin,
    TimeStampedModelMixin,
    AvatarModelMixin,
)


class Theorist(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel, AvatarModelMixin):
    """Model for business logic of web-site user. User model uses only for auth purposes."""

    PredefinedRankChoices = TheoristRankChoices

    # personal info
    full_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100, null=True, blank=True)

    full_name_slug = models.SlugField(max_length=255, null=True, blank=True)
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)

    # contact info urls
    social_media_url = models.URLField(max_length=225, null=True, blank=True)
    website_url = models.URLField(max_length=225, null=True, blank=True)

    # forum data
    total_posts = models.PositiveSmallIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    score = models.SmallIntegerField(default=0)
    rank = models.CharField(
        max_length=100,
        choices=PredefinedRankChoices,
        default=PredefinedRankChoices.JUNIOR,
    )

    last_activity = models.DateTimeField(auto_now=True)  # TODO: fix or remove

    class Meta:
        verbose_name = "theorist"
        verbose_name_plural = "theorists"

    def __str__(self):
        return f"{self.full_name} | {self.__class__.__name__} | id - {self.id}"

    def get_absolute_profile_url(self):
        return reverse(
            "forum:theorist_profile:base-page",
            kwargs={"pk": self.pk, "slug": self.full_name_slug},
        )

    def get_absolute_default_avatar_url(self):
        return None  # TODO: Add view with boringavatars URL

    @hook(BEFORE_SAVE)
    def before_save(self):
        slug = slugify(self.full_name)
        self.full_name_slug = slug
