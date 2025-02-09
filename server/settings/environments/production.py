# ruff: noqa: F405

from server.settings.common import *  # noqa: F403
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

CSRF_TRUSTED_ORIGINS = [""]

ALLOWED_HOSTS = ["127.0.0.1"]

# static
STATIC_ROOT = BASE_DIR / "templates/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
