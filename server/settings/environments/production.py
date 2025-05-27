# ruff: noqa: F405
from server.settings.common import *  # noqa: F403
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

SECRET_KEY = os.getenv('SECRET_KEY')

csrf_trusted_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = csrf_trusted_origins.split(',')

allowed_hosts = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = allowed_hosts.split(',')

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# AWS
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {'bucket_name': os.getenv('AWS_STORAGE_BUCKET_NAME'), 'location': 'media'},
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {'bucket_name': os.getenv('AWS_STORAGE_BUCKET_NAME'), 'location': 'static'},
    },
}

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_QUERYSTRING_AUTH = False
AWS_S3_REGION_NAME = 'eu-north-1'
