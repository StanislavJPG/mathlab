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
)

app_name = 'drafts'

urlpatterns = [
    path('drafts/', TheoristDraftsBaseTemplateView.as_view(), name='base-drafts'),
    path('drafts/album/<uuid:uuid>/', TheoristDraftsAlbumListView.as_view(), name='drafts-album-list'),
    path('drafts/table/<uuid:uuid>/', TheoristDraftsTableListView.as_view(), name='drafts-table-list'),
    path('hx/drafts/search/', HXTheoristDraftsSearchView.as_view(), name='drafts-search'),
    path('drafts/create/', TheoristDraftCreateView.as_view(), name='drafts-create'),
    path('drafts/update/<uuid:uuid>/', TheoristDraftUpdateView.as_view(), name='drafts-edit'),
    path('drafts/delete/<uuid:uuid>/', TheoristDraftDeleteView.as_view(), name='drafts-delete'),
]
