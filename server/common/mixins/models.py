import uuid
from typing import Final

from django.db import models
from django.utils import timezone
from django_lifecycle import hook, AFTER_SAVE
from dynamic_filenames import FilePattern
from easy_thumbnails.files import get_thumbnailer

from server.apps.forum.constants import MIN_SCORE, MAX_SCORE
from server.apps.theorist.choices import TheoristRankChoices
from server.common.third_party_apps.boringavatar import (
    BORINGAVATARS_DEFAULT_SIZE_QUALITY_LIST,
    BORINGAVATARS_DEFAULT_CROP,
)


class TimeStampedModelMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class UUIDModelMixin(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True


class RankSystemModelMixin(models.Model):
    PredefinedRankChoices = TheoristRankChoices
    PREDEFINED_MIN_SCORE = MIN_SCORE
    PREDEFINED_MAX_SCORE = MAX_SCORE

    rank = models.CharField(
        max_length=100,
        choices=PredefinedRankChoices,
        default=PredefinedRankChoices.JUNIOR,
    )
    score = models.SmallIntegerField(default=0)

    @hook(AFTER_SAVE, when='score', has_changed=True)
    def score_hook(self):
        if 100 <= self.score < 200:
            self.rank = self.PredefinedRankChoices.OLYMPIC
        elif 200 <= self.score < 300:
            self.rank = self.PredefinedRankChoices.TEACHER
        elif 300 <= self.score < 600:
            self.rank = self.PredefinedRankChoices.GURU
        elif self.score > 600:
            self.rank = self.PredefinedRankChoices.MATH_LORD
        else:
            return

        self.save(update_fields=['rank'])

    def add_min_score(self):
        # add minimum possible score
        self.score += self.PREDEFINED_MIN_SCORE
        self.save(update_fields=['score'])

    def add_max_score(self):
        # add maximum possible score
        self.score += self.PREDEFINED_MAX_SCORE
        self.save(update_fields=['score'])

    class Meta:
        abstract = True


upload_to_pattern_avatar = FilePattern(
    filename_pattern='{app_label:.25}/{instance.full_name_slug}/avatars/{uuid:s}{ext}'
)


class AvatarModelMixin(models.Model):
    AVATAR_DEFAULT_SIZE: Final[tuple] = (30, 30)
    AVATAR_DEFAULT_SQUARE: Final[bool] = False

    # custom avatar that was set by user
    custom_avatar = models.ImageField(max_length=600, upload_to=upload_to_pattern_avatar, blank=True, null=True)

    class Meta:
        abstract = True

    def get_boringavatars_url(self):
        """Returns default avatar's URL by unique identifier"""
        raise NotImplementedError(
            f'You need to specify a `get_boringavatars_url` method in your {self.__class__.__name__} model'
        )

    def get_current_avatar_url(self, size: tuple[int, int] = None, square: bool = None):
        if self.custom_avatar:
            # https://easy-thumbnails.readthedocs.io/en/latest/usage/?highlight=thumbnailer%20get_thumbnail#get-thumbnailer
            thumbnailer = get_thumbnailer(self.custom_avatar)
            thumb = thumbnailer.get_thumbnail(
                {
                    'size': BORINGAVATARS_DEFAULT_SIZE_QUALITY_LIST,
                    'crop': BORINGAVATARS_DEFAULT_CROP,
                }
            )
            avatar_url = thumb.url
        else:
            avatar_url = self.get_boringavatars_url() + f'?size={size[0]}&square={"true" if square else "false"}'
        return avatar_url

    def html_tag_avatar(self, size: tuple[int, int] = None, square: bool = None) -> str:
        """
        Generate HTML <img> tag for the avatar.
        """
        size = size or self.AVATAR_DEFAULT_SIZE
        square = square or self.AVATAR_DEFAULT_SQUARE
        avatar_url = self.get_current_avatar_url(size, square)

        return (
            f'<img src="{avatar_url}" width="{size[0]}" height="{size[1]}" '
            f'alt="avatar" class="{"rounded-circle" if not square else "squared"}">'
        )

    def drop_avatar_to_default(self):
        self.custom_avatar = None
        self.save(update_fields=['custom_avatar'])
