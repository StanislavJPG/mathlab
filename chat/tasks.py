from datetime import datetime, timedelta

from rest_framework import status

from mathlab.celery import app
from chat.models import Message


@app.task
def clear_deprecated_messages():
    try:
        one_week_ago = datetime.now() - timedelta(days=7)
        rows_to_delete = Message.objects.filter(sent_at__lte=one_week_ago)
        rows_to_delete.delete()
        return status.HTTP_200_OK
    except Exception:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
