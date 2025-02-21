from django.urls import path

from server.apps.forum.logic.posts import (
    PostCreateView,
    PostDetailView,
    PostDeleteView,
    HXPostLikesAndDislikesView,
    PostListView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path(
        'posts/<int:pk>/<slug:slug>/',
        PostDetailView.as_view(),
        name='post-details',
    ),
    path(
        '<uuid:uuid>/posts/delete/',
        PostDeleteView.as_view(),
        name='post-delete',
    ),
    path(
        'posts/create/',
        PostCreateView.as_view(),
        name='post-create',
    ),
    path(
        '<uuid:uuid>/posts/rate/',
        HXPostLikesAndDislikesView.as_view(),
        name='hx-post-rate',
    ),
]
