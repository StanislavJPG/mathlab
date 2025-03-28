import random

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
