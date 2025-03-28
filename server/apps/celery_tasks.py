from celery.schedules import crontab

from server.common.utils import celery


@celery.periodic_tasks_args
def provide_tasks():
    """
    pattern: ('task_dir', schedule, args(optionally))
    """

    return (('server.apps.math_news.tasks.create_news_task', crontab(hour=7, minute=30)),)
