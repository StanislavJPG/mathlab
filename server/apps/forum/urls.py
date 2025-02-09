from django.urls import path

from server.apps.forum.views import ForumBaseView, QuestionCreationView, QuestionView
from server.apps.users.views import ProfileView, ChangeUserDataView

urlpatterns = [
    path("forum/", ForumBaseView.as_view(), name="forum-base"),
    path(
        "profile/<int:user_id>/<str:username>",
        ProfileView.as_view(),
        name="forum-profile",
    ),
    path(
        "forum/create-question/",
        QuestionCreationView.as_view(),
        name="forum-q-creation",
    ),
    path(
        "forum/question/<int:q_id>/<str:title>/",
        QuestionView.as_view({"post": "create_comment"}),
        name="forum-q",
    ),
    path(
        "forum/question/rate/<int:q_id>/<str:title>/",
        QuestionView.as_view({"post": "create_post_rate"}),
        name="forum-q-rate",
    ),
    path(
        "forum/question/comment/rate/<int:q_id>/<str:title>/",
        QuestionView.as_view({"post": "create_comment_rate"}),
        name="forum-q-comm-rate",
    ),
    path(
        "forum/question/comment/delete/<int:q_id>/<str:title>/<int:comment_id>/",
        QuestionView.as_view({"post": "delete_comment"}),
        name="forum-q-comm-delete",
    ),
    path("forum/settings/", ChangeUserDataView.as_view(), name="forum-settings"),
]
