from django.urls import path

from server.apps.forum.views.comments import (
    CommentCreateView,
    CommentDeleteView,
    CommentQuantityView,
)
from server.apps.forum.views.forum_base import ForumBaseView
from server.apps.forum.views.posts import (
    PostCreateView,
    PostView,
    PostDeleteView,
)
from server.apps.forum.views.profile import ProfileView
from server.apps.users.views.profile_settings import ChangeUserDataView

urlpatterns = [
    # Forum base block
    path("", ForumBaseView.as_view(), name="base"),
    # Question posts block
    path(
        "question/<int:pk>/<slug:slug>/",
        PostView.as_view(),
        name="question-post-base",
    ),
    path(
        "questions/delete/<uuid:uuid>/",
        PostDeleteView.as_view(),
        name="question-delete",
    ),
    path(
        "questions/create/",
        PostCreateView.as_view(),
        name="question-create",
    ),
    # path(
    #     "forum/question/rate/<int:q_id>/<str:title>/",
    #     QuestionView.as_view({"post": "create_post_rate"}),
    #     name="q-rate",
    # ),
    # Question comments block
    path(
        "comment/create/<uuid:post_uuid>/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comment/delete/<uuid:uuid>/<uuid:post_uuid>/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    # path(
    #     "forum/question/comment/rate/<int:q_id>/<str:title>/",
    #     QuestionView.as_view({"post": "create_comment_rate"}),
    #     name="q-comm-rate",
    # ),
    path(
        "comment/count/<uuid:post_uuid>/",
        CommentQuantityView.as_view(),
        name="comments-count",
    ),
    # Profile block
    path(
        "profile/<int:user_id>/<str:username>",
        ProfileView.as_view(),
        name="profile",
    ),
    # User data block
    path("forum/settings/", ChangeUserDataView.as_view(), name="settings"),
]
