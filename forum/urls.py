from django.urls import path, include

from forum.views import ForumBaseView, forum_topics, ProfileView, QuestionCreationView, QuestionView

urlpatterns = [
    path('forum/', ForumBaseView.as_view(), name='forum-base'),
    path('forum/topics/', forum_topics, name='forum-topics'),
    path('profile/<int:user_id>/<str:username>', ProfileView.as_view(), name='forum-profile'),
    path('forum/create-question/', QuestionCreationView.as_view(), name='forum-q-creation'),
    path('forum/question/<int:q_id>/<str:title>/', QuestionView.as_view(), name='forum-q'),
]
