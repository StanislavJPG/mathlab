# ruff: noqa: F405
from server.settings.common import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.0.110']

CSRF_TRUSTED_ORIGINS = ['127.0.0.1', 'localhost', '192.168.0.110']

SECRET_KEY = 'ASOJFAOSJ-0J1-0U-0js0adja0sj0-21juu0--109U2U0@((@(@'

INSTALLED_APPS += ['debug_toolbar', 'django_lifecycle_checks', 'django_extensions']

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

MIDDLEWARE += [
    # uncomment to debug
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    '127.0.0.1',
]

STATICFILES_DIRS = [BASE_DIR / 'static/']

# Media
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')
MEDIA_URL = '/media/'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}
