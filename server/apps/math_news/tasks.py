from django.db import IntegrityError
from rest_framework import status

from server.apps.math_news.models import MathNews
from server.apps.math_news.scraper import MathNewsSearcher
from server.apps.mathlab.celery import app


@app.task
def let_find_news():
    titles = MathNewsSearcher()
    try:
        for title in titles:
            MathNews.objects.create(
                title=title['title'],
                new_url=title['new_url'],
                posted=title['posted'],
                additional_info=title['add_info'],
            )
        return status.HTTP_201_CREATED
    except IntegrityError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
