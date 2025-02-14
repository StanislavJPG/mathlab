from django.urls import path

from server.apps.forum.views.comments import (
    CommentCreateView,
    CommentDeleteView,
    HXCommentQuantityView,
    HXCommentLikesAndDislikesView,
    CommentListView,
)
from server.apps.forum.views.posts import (
    PostCreateView,
    PostDetailView,
    PostDeleteView,
    HXPostLikesAndDislikesView,
    PostListView,
)
from server.apps.forum.views.profile import ProfileView
from server.apps.users.views.profile_settings import ChangeUserDataView

urlpatterns = [
    # Forum base block
    path("", PostListView.as_view(), name="base"),
    # Question posts block
    path(
        "question/<int:pk>/<slug:slug>/",
        PostDetailView.as_view(),
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
    path(
        "questions/rate/<uuid:uuid>/",
        HXPostLikesAndDislikesView.as_view(),
        name="hx-question-rate",
    ),
    # Question comments block
    path(
        "comments/<uuid:post_uuid>/",
        CommentListView.as_view(),
        name="comments-block",
    ),
    path(
        "comments/create/<uuid:post_uuid>/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comments/delete/<uuid:uuid>/<uuid:post_uuid>/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path(
        "comments/count/<uuid:post_uuid>/",
        HXCommentQuantityView.as_view(),
        name="comments-count",
    ),
    path(
        "comments/rate/<uuid:uuid>/",
        HXCommentLikesAndDislikesView.as_view(),
        name="hx-comment-rate",
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
