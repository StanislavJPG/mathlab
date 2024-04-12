from django.urls import path

from forum.views import forum_base, forum_topics, ProfileView, QuestionCreationView

urlpatterns = [
    path('forum/', forum_base, name='forum-base'),
    path('forum/topics/', forum_topics, name='forum-topics'),
    path('profile/', ProfileView.as_view(), name='forum-profile'),
    path('forum/create-question/', QuestionCreationView.as_view(), name='forum-q-creation'),
]
