from django.urls import path

from server.apps.forum.logic.posts import (
    PostDetailView,
    HXPostLikesAndDislikesView,
    PostListView,
    PostSupportUpdateView,
    PostDefaultImageView,
    BasePostTemplateView,
)
from server.apps.forum.logic.post_management import (
    PostCreateBaseView,
    PostCreateView,
    PostDeleteView,
    PostContentUpdateView,
    PostTitleUpdateView,
)

urlpatterns = [
    path('', BasePostTemplateView.as_view(), name='base-forum-page'),
    path('posts/list/', PostListView.as_view(), name='post-list'),
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
        PostCreateBaseView.as_view(),
        name='post-create',
    ),
    path(
        'hx/posts/create/',
        PostCreateView.as_view(),
        name='hx-post-create',
    ),
    path(
        'hx/<uuid:uuid>/posts/content/update/',
        PostContentUpdateView.as_view(),
        name='hx-post-content-update',
    ),
    path(
        'hx/<uuid:uuid>/posts/title/update/',
        PostTitleUpdateView.as_view(),  # TODO: Change redirect to dynamic reswap
        name='hx-post-title-update',
    ),
    path(
        '<uuid:uuid>/posts/rate/',
        HXPostLikesAndDislikesView.as_view(),
        name='hx-post-rate',
    ),
    path(
        '<uuid:uuid>/posts/support/',
        PostSupportUpdateView.as_view(),
        name='posts-support-update',
    ),
    # avatars
    path(
        '<uuid:uuid>/posts/avatar/',
        PostDefaultImageView.as_view(),
        name='post-avatar',
    ),
]
