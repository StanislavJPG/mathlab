from django.urls import path

from server.apps.math_news.logic.news import NewsBaseTemplateView, NewsListView

app_name = 'math_news'

urlpatterns = [
    path('news/', NewsBaseTemplateView.as_view(), name='base-math-news'),
    path('hx/news/list/', NewsListView.as_view(), name='hx-math-news-list'),
]
