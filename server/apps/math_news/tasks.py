from server.apps.math_news.models import MathNews
from server.apps.math_news.scraper import MathNewsSearcher


# @app.task
def create_news_task():
    titles = MathNewsSearcher()
    for title in titles:
        MathNews.objects.create(
            title=title['title'],
            origin_url=title['new_url'],
            # published_at=title['posted'],
            short_content=title['add_info'],
        )
    return


# @app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, create_news_task.s(), name='Create News')
