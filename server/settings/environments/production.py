# ruff: noqa: F405
from server.settings.common import *  # noqa: F403
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

CSRF_TRUSTED_ORIGINS = ['']

ALLOWED_HOSTS = ['']

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# TODO: Change by correct urls
MEDIA_URL = 'https://your-cdn.example.com/media/'

STATIC_ROOT = BASE_DIR.parent / 'staticfiles'

# static
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
