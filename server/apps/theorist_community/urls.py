from django.urls import path

from server.apps.theorist_community.logic.community import TheoristCommunityBaseTemplateView

app_name = 'theorist_community'

urlpatterns = [
    path('all/', TheoristCommunityBaseTemplateView.as_view(), name='all'),
]
