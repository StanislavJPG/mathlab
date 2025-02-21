import uuid
from typing import Final

from django.db import models
from django.utils import timezone
from dynamic_filenames import FilePattern
from easy_thumbnails.files import get_thumbnailer

from server.common.third_party_apps.boringavatar import (
    BORINGAVATARS_DEFAULT_SIZE_QUALITY,
    BORINGAVATARS_DEFAULT_CROP,
)


class TimeStampedModelMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class UUIDModelMixin(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

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

    def get_absolute_default_avatar_url(self):
        """Returns default avatar's URL by unique identifier"""
        raise NotImplementedError(
            f'You need to specify a get_absolute_default_avatar_url method in your {self.__class__.__name__} model'
        )

    def html_tag_avatar(self, size: tuple[int, int] = None, square: bool = None) -> str:
        """
        Generate an HTML <img> tag for the avatar.
        """
        size = size or self.AVATAR_DEFAULT_SIZE
        square = square or self.AVATAR_DEFAULT_SQUARE

        if self.custom_avatar:
            # https://easy-thumbnails.readthedocs.io/en/latest/usage/?highlight=thumbnailer%20get_thumbnail#get-thumbnailer
            thumbnailer = get_thumbnailer(self.custom_avatar)
            thumbnail = thumbnailer.get_thumbnail(
                {
                    'size': BORINGAVATARS_DEFAULT_SIZE_QUALITY,
                    'crop': BORINGAVATARS_DEFAULT_CROP,
                }
            )
            avatar_url = thumbnail.url
        else:
            avatar_url = (
                self.get_absolute_default_avatar_url() + f'?size={size[0]}&square={"true" if square else "false"}'
            )

        return (
            f'<img src="{avatar_url}" width="{size[0]}" height="{size[1]}" '
            f'alt="avatar" class="{"rounded-circle" if square else "squared"}">'
        )

    def drop_avatar_to_default(self):
        self.custom_avatar = None
        self.save(update_fields=['custom_avatar'])
