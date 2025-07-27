from datetime import timedelta

from celery.schedules import crontab

from celery_simple_schedule import simplify_schedules


@simplify_schedules
def provide_tasks():
    return (
        ('server.apps.math_news.tasks.create_news_task', crontab(hour=7, minute=30)),
        ('server.apps.theorist_notifications.tasks.clear_expired_deleted_notifications', timedelta(days=3)),
    )
