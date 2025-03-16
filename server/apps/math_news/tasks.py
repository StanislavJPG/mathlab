from celery.schedules import crontab

from server.apps.math_news.scraper import MathNewsSearcher
from server.settings.celery import app


@app.task
def create_news_task():
    titles = MathNewsSearcher()
    titles.save_news()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=7, minute=30), create_news_task.s(), name='create_news')
