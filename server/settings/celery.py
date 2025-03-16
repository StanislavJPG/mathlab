import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.environments.development')
app = Celery('mathlab', broker=f'redis://redis:{os.getenv("REDIS_PORT")}')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
