import collections
import random
import re

import uuid
from typing import Union

from PIL import Image
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.files import get_thumbnailer


def generate_randon_hex_colors(number_of_colors: int) -> list:
    # thanks to https://stackoverflow.com/a/50218895/22892730
    colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(number_of_colors)]
    return colors


def is_valid_uuid(uuid_to_test):
    try:
        # check for validity of Uuid
        uuid.UUID(uuid_to_test)
    except ValueError:
        return False
    return True


def is_iterable(x):
    return isinstance(x, collections.abc.Iterable)


def limit_nbsp_paragraphs(html: str, max_count: int = 3) -> str:
    # Pattern for repeated <p>&nbsp;</p> blocks (with optional whitespace)
    pattern = r'(?:<p>\s*&nbsp;\s*</p>\s*){' + str(max_count + 1) + r',}'
    replacement = ('<p>&nbsp;</p>\n' * max_count).strip()
    html = re.sub(pattern, replacement, html)

    text_only = re.sub(r'<[^>]*>', '', html)
    text_only = re.sub(r'&nbsp;', ' ', text_only)

    if not text_only.strip():
        return ''

    return html


def format_relative_time(diff_time):
    t = timezone.now() - diff_time
    sent = t.seconds
    if sent <= 30:
        return _('Just now')
    elif 60 <= sent <= 300:
        return _('Couple minutes ago')
    elif 300 < sent <= 400:
        return _('5 minutes ago')
    elif t.days < 1:
        return timezone.localtime(diff_time).time()
    else:
        return diff_time


class ConvenientImage:
    """
    Transform image field into `ConvenientImage` object
    to conveniently get processed image attributes
    """

    def __init__(self, img_field, size: Union[list, tuple] = None, **kwargs):
        self.kwargs = kwargs

        if not size:
            with Image.open(img_field) as img:
                width, height = img.size
        else:
            width, height = size
        thumbnailer = get_thumbnailer(img_field)
        thumb = thumbnailer.get_thumbnail({'size': (width, height), **self._get_kwargs()})
        self.url: str = thumb.url
        self.width: int = width
        self.height: int = height

    def _get_kwargs(self):
        return self.kwargs or {
            'crop': False,
            'upscale': False,
        }
