from server.apps.math_news.models import MathNews
from server.apps.math_news.scraper import MathNewsSearcher
from server.settings.celery import app


@app.task
def create_news_task():
    titles = MathNewsSearcher()
    MathNews.save_unique_news(titles.kwargs_list)
