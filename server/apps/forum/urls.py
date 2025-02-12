from django.urls import path

from server.apps.forum.views.forum_base import ForumBaseView
from server.apps.forum.views.questions import (
    QuestionCreationView,
    QuestionView,
    QuestionDeleteView,
)
from server.apps.forum.views.profile import ProfileView
from server.apps.users.views.profile_settings import ChangeUserDataView

urlpatterns = [
    path("", ForumBaseView.as_view(), name="base"),
    path(
        "questions/<int:id>/delete",
        QuestionDeleteView.as_view(),
        name="question-delete",
    ),
    path(
        "profile/<int:user_id>/<str:username>",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "forum/create-question/",
        QuestionCreationView.as_view(),
        name="q-creation",
    ),
    path(
        "forum/question/<int:q_id>/<str:title>/",
        QuestionView.as_view({"post": "create_comment"}),
        name="q",
    ),
    path(
        "forum/question/rate/<int:q_id>/<str:title>/",
        QuestionView.as_view({"post": "create_post_rate"}),
        name="q-rate",
    ),
    path(
        "forum/question/comment/rate/<int:q_id>/<str:title>/",
        QuestionView.as_view({"post": "create_comment_rate"}),
        name="q-comm-rate",
    ),
    path(
        "forum/question/comment/delete/<int:q_id>/<str:title>/<int:comment_id>/",
        QuestionView.as_view({"post": "delete_comment"}),
        name="q-comm-delete",
    ),
    path("forum/settings/", ChangeUserDataView.as_view(), name="settings"),
]
