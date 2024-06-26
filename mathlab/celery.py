from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

from mathlab import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mathlab.settings')

app = Celery('mathlab')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

