import logging.config
import os
import sys

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = reverse_lazy('users:base-auth')

SITE_ID = 1
SITE_DEFAULT_URL = reverse_lazy('forum:base-forum-page')

MODELS_TO_ICONS = (
    ('theorist_drafts.TheoristDraftsConfiguration', 'ti ti-file-pencil'),
    ('theorist_chat.TheoristMessage', 'ti ti-mail'),
    ('theorist.TheoristFriendship', 'ti ti-friends'),
    ('forum.Comment', 'ti ti-message-circle'),
    ('forum.Post', 'ti ti-article'),
)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_FULL_URL', f'redis://redis:{os.getenv("REDIS_PORT")}'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'server.common.middlewares.RequestLoggingMiddleware': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
logging.config.dictConfig(LOGGING)


MESSAGE_TAGS = {messages.ERROR: 'danger', messages.SUCCESS: 'success'}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('MAIL_NAME')
EMAIL_HOST_PASSWORD = os.getenv('MAIL_PASS')
