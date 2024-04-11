from django.urls import path

from forum.views import forum_base, forum_topics

urlpatterns = [
    path('forum/', forum_base, name='forum-base'),
    path('forum/topics/', forum_topics, name='forum-topics')
]
