from django.core.cache import cache


def delete_keys_matching_pattern(*pattern):
    patterns = pattern if isinstance(pattern, tuple) else (pattern,)

    for pattern_key in patterns:
        keys_to_delete = cache.keys(pattern_key)
        cache.delete_many(keys_to_delete)
