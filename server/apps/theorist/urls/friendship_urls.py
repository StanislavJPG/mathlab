from django.urls import path

from server.apps.theorist.logic.friendship.friends import (
    HXTheoristFriendshipListView,
    HXTheoristFriendshipTemplateView,
    HXTheoristPrivateCommunityListView,
    TheoristPrivateCommunityTemplateView,
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
]
