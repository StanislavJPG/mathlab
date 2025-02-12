from django.urls import path

from server.apps.forum.views.forum_base import ForumBaseView
from server.apps.forum.views.questions import (
    QuestionCreateView,
    QuestionView,
    QuestionDeleteView,
)
from server.apps.forum.views.profile import ProfileView
from server.apps.users.views.profile_settings import ChangeUserDataView

urlpatterns = [
    # Forum base block
    path("", ForumBaseView.as_view(), name="base"),
    # Question posts block
    path(
        "questions/<int:id>/delete/",
        QuestionDeleteView.as_view(),
        name="question-delete",
    ),
    path(
        "questions/create/",
        QuestionCreateView.as_view(),
        name="question-create",
    ),
    # path(
    #     "forum/question/rate/<int:q_id>/<str:title>/",
    #     QuestionView.as_view({"post": "create_post_rate"}),
    #     name="q-rate",
    # ),
    # Question comments block
    path(
        "forum/question/<int:pk>/<slug:slug>/",
        QuestionView.as_view(),
        name="q",
    ),
    # path(
    #     "forum/question/comment/delete/<int:q_id>/<str:title>/<int:comment_id>/",
    #     QuestionView.as_view({"post": "delete_comment"}),
    #     name="q-comm-delete",
    # ),
    # path(
    #     "forum/question/comment/rate/<int:q_id>/<str:title>/",
    #     QuestionView.as_view({"post": "create_comment_rate"}),
    #     name="q-comm-rate",
    # ),
    # Profile block
    path(
        "profile/<int:user_id>/<str:username>",
        ProfileView.as_view(),
        name="profile",
    ),
    # User data block
    path("forum/settings/", ChangeUserDataView.as_view(), name="settings"),
]
