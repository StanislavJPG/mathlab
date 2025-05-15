from datetime import timedelta

from django.utils import timezone

from server.apps.theorist_notifications.models import TheoristNotification
from server.settings.celery import app


@app.task
def clear_expired_deleted_notifications():
    threshold = timezone.now() - timedelta(days=3)
    deleted_notifications = TheoristNotification.objects.filter(timestamp__lt=threshold).deleted()
    return deleted_notifications.delete()
