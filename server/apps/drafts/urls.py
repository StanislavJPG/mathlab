from django.urls import path

from server.apps.drafts.logic.drafts import TheoristDraftsBaseTemplateView

app_name = 'drafts'

urlpatterns = [
    path('drafts/<slug:full_name_slug>/', TheoristDraftsBaseTemplateView.as_view(), name='base-drafts'),
]
