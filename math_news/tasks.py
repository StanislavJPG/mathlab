from django.db import IntegrityError
from rest_framework import status

from math_news.models import MathNews
from math_news.scraper import MathNewsSearcher
from mathlab.celery import app


@app.task
def let_find_news():
    titles = MathNewsSearcher()
    try:
        for title in titles:
            MathNews.objects.create(
                title=title['title'],
                new_url=title['new_url'],
                posted=title['posted'],
                additional_info=title['add_info']
            )
        return status.HTTP_201_CREATED
    except IntegrityError:
        return status.HTTP_409_CONFLICT
