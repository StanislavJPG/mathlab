import os

from celery import Celery

from server.apps.celery_tasks import provide_tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.environments.development')
broker = os.getenv('REDIS_FULL_URL', f'redis://redis:{os.getenv("REDIS_PORT")}')

app = Celery('mathlab', broker=broker)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = provide_tasks()
