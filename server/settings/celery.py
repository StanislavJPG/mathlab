import os

from datetime import timedelta

__all__ = (
    'CELERY_BROKER_URL',
    'CELERY_RESULT_BACKEND',
    'CELERY_IMPORTS',
    'CELERY_BEAT_SCHEDULE',
)

CELERY_BROKER_URL = f'redis://redis:{os.getenv("REDIS_PORT")}'
CELERY_RESULT_BACKEND = f'redis://redis:{os.getenv("REDIS_PORT")}'
CELERY_IMPORTS = ['server.apps.math_news.tasks', 'server.apps.chat.tasks']

CELERY_BEAT_SCHEDULE = {
    'to_find_news': {
        'task': 'server.apps.math_news.tasks.let_find_news',
        'schedule': timedelta(minutes=1),
    },
    'clear_garbage': {
        'task': 'server.apps.chat.tasks.clear_deprecated_messages',
        'schedule': timedelta(days=7),
    },
}
