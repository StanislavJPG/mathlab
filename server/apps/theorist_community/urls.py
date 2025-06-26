from django.urls import path

from server.apps.theorist_community.logic.community import (
    TheoristCommunityBaseTemplateView,
    HXTheoristCommunityBaseListView,
    HXTheoristCommunityFriendshipBlockView,
)

app_name = 'theorist_community'

urlpatterns = [
    path('all/', TheoristCommunityBaseTemplateView.as_view(), name='all'),
    path('hx/base-list/', HXTheoristCommunityBaseListView.as_view(), name='hx-base-list'),
    path(
        'hx/<uuid:uuid>/friendship-block/', HXTheoristCommunityFriendshipBlockView.as_view(), name='hx-friendship-block'
    ),
]
