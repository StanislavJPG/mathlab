from server.apps.math_news.scraper import MathNewsSearcher
from server.settings.celery import app


@app.task
def create_news_task():
    titles = MathNewsSearcher()
    titles.save_news()
