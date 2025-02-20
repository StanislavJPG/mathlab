from django.urls import path

from server.apps.forum.logic.comments import (
    CommentCreateView,
    CommentDeleteView,
    HXCommentQuantityView,
    HXCommentLikesAndDislikesView,
    CommentListView,
)

urlpatterns = [
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
]
