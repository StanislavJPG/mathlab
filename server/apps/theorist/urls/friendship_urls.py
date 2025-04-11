from django.urls import path

from server.apps.theorist.logic.friends import HXTheoristFriendshipListView

app_name = 'friendship'

urlpatterns = [
    path(
        '<uuid:uuid>/list/',
        HXTheoristFriendshipListView.as_view(),
        name='hx-theorist-friends-list',
    ),
]
