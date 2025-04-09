import random
import re

import uuid


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
