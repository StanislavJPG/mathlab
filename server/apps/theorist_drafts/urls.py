from django.urls import path

from server.apps.theorist_drafts.logic.drafts import (
    TheoristDraftsBaseTemplateView,
    TheoristDraftsAlbumListView,
    TheoristDraftsTableListView,
    HXTheoristDraftsSearchView,
)
from server.apps.theorist_drafts.logic.drafts_management import (
    TheoristDraftCreateView,
    TheoristDraftDeleteView,
    TheoristDraftUpdateView,
    TheoristDraftUploadView,
)

app_name = 'drafts'

urlpatterns = [
    path('drafts/', TheoristDraftsBaseTemplateView.as_view(), name='base-drafts'),
    path(
        'drafts/album/<uuid:drafts_configuration_uuid>/',
        TheoristDraftsAlbumListView.as_view(),
        name='drafts-album-list',
    ),
    path(
        'drafts/table/<uuid:drafts_configuration_uuid>/',
        TheoristDraftsTableListView.as_view(),
        name='drafts-table-list',
    ),
    path('hx/drafts/search/', HXTheoristDraftsSearchView.as_view(), name='drafts-search'),
    path('drafts/create/', TheoristDraftCreateView.as_view(), name='drafts-create'),
    path('drafts/update/<uuid:uuid>/', TheoristDraftUpdateView.as_view(), name='drafts-edit'),
    path('drafts/upload/', TheoristDraftUploadView.as_view(), name='drafts-upload'),
    path('drafts/delete/<uuid:uuid>/', TheoristDraftDeleteView.as_view(), name='drafts-delete'),
]
