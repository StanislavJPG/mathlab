from django.urls import path

from server.apps.theorist.logic.friendship.blacklist import (
    HXTheoristBlacklistView,
    TheoristUnblockFromBlacklistView,
    TheoristBlockView,
)
from server.apps.theorist.logic.friendship.friends import (
    HXTheoristFriendshipListView,
    HXTheoristFriendshipTemplateView,
    HXTheoristPrivateCommunityListView,
    TheoristPrivateCommunityTemplateView,
    HXCommunityListCounters,
)
from server.apps.theorist.logic.friendship.friends_management import (
    TheoristFriendshipCreateView,
    TheoristAcceptFriendshipView,
    TheoristBrokeUpFriendshipView,
    TheoristRejectFriendshipView,
)

app_name = 'friendship'

urlpatterns = [
    path(
        '<uuid:uuid>/friendship/',
        HXTheoristFriendshipTemplateView.as_view(),
        name='hx-theorist-friendship',
    ),
    path(
        'hx/<uuid:theorist_uuid>/<str:status>/list/',
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
    path(
        'hx/my-community/navs-counters/',
        HXCommunityListCounters.as_view(),
        name='hx-theorist-community-list-navs-counters',
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
    path(
        'hx/<uuid:uuid>/reject-friendship/',
        TheoristRejectFriendshipView.as_view(),
        name='theorist-friendship-reject',
    ),
    path(
        'hx/<uuid:uuid>/brokeup-friendship/',
        TheoristBrokeUpFriendshipView.as_view(),
        name='theorist-friendship-broke-up',
    ),
    # Blacklist urls
    path(
        'hx/my-community/blacklist/',
        HXTheoristBlacklistView.as_view(),
        name='hx-theorist-community-blacklist',
    ),
    path(
        'hx/<uuid:uuid>/my-community/blacklist/<uuid:theorist_uuid>/unblock/',
        TheoristUnblockFromBlacklistView.as_view(),
        name='theorist-blacklist-unblock',
    ),
    path(
        'hx/<uuid:uuid>/my-community/blacklist/<uuid:theorist_uuid>/block/',
        TheoristBlockView.as_view(),
        name='theorist-blacklist-block',
    ),
]
