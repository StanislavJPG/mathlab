from django.urls import path

from server.apps.theorist.logic.friendship.friends import (
    HXTheoristFriendshipListView,
    HXTheoristFriendshipTemplateView,
    HXTheoristPrivateCommunityListView,
    TheoristPrivateCommunityTemplateView,
)
from server.apps.theorist.logic.friendship.friends_management import (
    TheoristFriendshipCreateView,
    TheoristAcceptFriendshipView,
)

app_name = 'friendship'

urlpatterns = [
    path(
        '<uuid:uuid>/friendship/',
        HXTheoristFriendshipTemplateView.as_view(),
        name='hx-theorist-friendship',
    ),
    path(
        'hx/<uuid:uuid>/<str:status>/list/',
        HXTheoristFriendshipListView.as_view(),
        name='hx-theorist-friends-list',
    ),
    path(
        'my-community/list/',
        TheoristPrivateCommunityTemplateView.as_view(),
        name='theorist-community-list',
    ),
    path(
        'hx/<str:status>/my-community/list/',
        HXTheoristPrivateCommunityListView.as_view(),
        name='hx-theorist-community-list',
    ),
    # Management urls
    path(
        'hx/<uuid:theorist_uuid>/request/',
        TheoristFriendshipCreateView.as_view(),
        name='theorist-friendship-request',
    ),
    path(
        'hx/<uuid:uuid>/accept-pending/',
        TheoristAcceptFriendshipView.as_view(),
        name='theorist-friendship-accept',
    ),
]
