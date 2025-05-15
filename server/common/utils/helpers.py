import random
import re

import uuid

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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


def get_icon_for_contenttype_model(contenttype_obj):
    to_return = None
    try:
        for instance in settings.MODELS_TO_ICONS:
            if f'{contenttype_obj.app_label}.{contenttype_obj.model}' == instance[0].lower():
                to_return = instance[1]
    except AttributeError:
        raise TypeError('contenttype_obj must be an instance of ContentType')

    if not to_return:
        raise NotImplementedError('Model "{}" not found in `settings.MODELS_TO_ICONS`.'.format(contenttype_obj.model))
    return to_return


def get_page_for_paginated_obj(
    obj,
    child_obj,
    child_paginated_objs_label: str,
    paginate_by: int,
    ordered_by: str,
):
    if hasattr(obj, child_paginated_objs_label):
        siblings_qs = getattr(obj, child_paginated_objs_label).all().order_by(ordered_by)
        ids = list(siblings_qs.values_list('id', flat=True))

        try:
            index = ids.index(child_obj.id)
        except ValueError:
            return None

        page_number = (index // paginate_by) + 1
        return page_number
