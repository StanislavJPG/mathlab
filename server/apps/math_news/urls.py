from django.urls import path

from server.apps.math_news.logic.news import NewsView

urlpatterns = [
    path('news/math/', NewsView.as_view(), name='base-math-news'),
]
