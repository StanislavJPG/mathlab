from django.urls import path

from server.apps.forum.logic.comments import (
    CommentCreateView,
    CommentDeleteView,
    HXCommentQuantityView,
    HXCommentLikesAndDislikesView,
    CommentListView,
)
from server.apps.forum.logic.posts import (
    PostCreateView,
    PostDetailView,
    PostDeleteView,
    HXPostLikesAndDislikesView,
    PostListView,
)
from server.apps.forum.logic.profile import ProfileDetailView
from server.apps.users.logic.profile_settings import ChangeUserDataView

urlpatterns = [
    # Posts block
    path("", PostListView.as_view(), name="post-list"),
    path(
        "posts/<int:pk>/<slug:slug>/",
        PostDetailView.as_view(),
        name="post-details",
    ),
    path(
        "<uuid:uuid>/posts/delete/",
        PostDeleteView.as_view(),
        name="post-delete",
    ),
    path(
        "posts/create/",
        PostCreateView.as_view(),
        name="post-create",
    ),
    path(
        "<uuid:uuid>/posts/rate/",
        HXPostLikesAndDislikesView.as_view(),
        name="hx-post-rate",
    ),
    # Question comments block
    path(
        "comments/<uuid:post_uuid>/",
        CommentListView.as_view(),
        name="comments-block",
    ),
    path(
        "<uuid:post_uuid>/comments/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "<uuid:uuid>/comments/<uuid:post_uuid>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path(
        "<uuid:post_uuid>/comments/count/",
        HXCommentQuantityView.as_view(),
        name="comments-count",
    ),
    path(
        "<uuid:uuid>/comments/rate/",
        HXCommentLikesAndDislikesView.as_view(),
        name="hx-comment-rate",
    ),
    # Profile block
    path(
        "profile/details/<int:pk>/<str:username>/",
        ProfileDetailView.as_view(),
        name="profile-details",
    ),
    # User data block
    path("profile/settings/", ChangeUserDataView.as_view(), name="profile-settings"),
]
