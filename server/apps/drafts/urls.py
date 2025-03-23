from django.urls import path

from server.apps.drafts.logic.drafts import (
    TheoristDraftsBaseTemplateView,
    TheoristDraftsAlbumListView,
    TheoristDraftCreateView,
    TheoristDraftsTableListView,
)

app_name = 'drafts'

urlpatterns = [
    path('drafts/', TheoristDraftsBaseTemplateView.as_view(), name='base-drafts'),
    path('drafts/album/<uuid:uuid>/', TheoristDraftsAlbumListView.as_view(), name='drafts-album-list'),
    path('drafts/table/<uuid:uuid>/', TheoristDraftsTableListView.as_view(), name='drafts-table-list'),
    path('drafts/create/', TheoristDraftCreateView.as_view(), name='drafts-create'),
]
