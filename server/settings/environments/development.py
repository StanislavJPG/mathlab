# ruff: noqa: F405
from server.settings.common import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# CSRF_TRUSTED_ORIGINS = ['']

SECRET_KEY = "ASOJFAOSJ-0J1-0U-0js0adja0sj0-21juu0--109U2U0@((@(@"

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    # uncomment to debug
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}
