from django.urls import path

from server.apps.theorist.logic.friends import HXTheoristFriendshipListView, HXTheoristFriendshipTemplateView

app_name = 'friendship'

urlpatterns = [
    path(
        '<uuid:uuid>/friendship/',
        HXTheoristFriendshipTemplateView.as_view(),
        name='hx-theorist-friendship',
    ),
    path(
        '<uuid:uuid>/<str:status>/list/',
        HXTheoristFriendshipListView.as_view(),
        name='hx-theorist-friends-list',
    ),
]
