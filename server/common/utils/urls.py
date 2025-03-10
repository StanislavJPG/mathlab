from server.common.constants import ACCESSED_ONBOARDING_START_PREFIXES_URLS


def is_excluded_path(request):
    excluded_paths = ACCESSED_ONBOARDING_START_PREFIXES_URLS
    return any(request.path.startswith(excluded) for excluded in excluded_paths)
