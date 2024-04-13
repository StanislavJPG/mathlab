from django.urls import path

from forum.views import ForumBaseView, forum_topics, ProfileView, QuestionCreationView

urlpatterns = [
    path('forum/', ForumBaseView.as_view(), name='forum-base'),
    path('forum/topics/', forum_topics, name='forum-topics'),
    path('profile/<int:user_id>', ProfileView.as_view(), name='forum-profile'),
    path('forum/create-question/', QuestionCreationView.as_view(), name='forum-q-creation'),
]
