# ruff: noqa: F405
from server.settings.common import *  # noqa: F403

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.0.110']

CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1:8000', 'https://localhost:8000', 'https://192.168.0.110:8000']

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

DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG, 'IS_RUNNING_TESTS': False}
