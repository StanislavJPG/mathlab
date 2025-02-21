from django.urls import path

from server.apps.theorist.logic.profile import (
    TheoristProfileDetailView,
    HXTheoristDetailsProfileView,
    TheoristLastActivitiesListView,
)
from server.apps.users.logic.profile_settings import TheoristSettingsDetailView

app_name = 'theorist_profile'

urlpatterns = [
    path(
        '<int:pk>/<slug:full_name_slug>/',
        TheoristProfileDetailView.as_view(),
        name='base-page',
    ),
    path(
        '<int:pk>/<slug:full_name_slug>/<str:section>/',
        HXTheoristDetailsProfileView.as_view(),
        name='hx-theorist-details',
    ),
    path(
        '<uuid:uuid>/last-activities/',
        TheoristLastActivitiesListView.as_view(),
        name='hx-theorist-last-activities',
    ),
    path(
        'settings/<uuid:uuid>/',
        TheoristSettingsDetailView.as_view(),
        name='theorist-settings',
    ),  # TODO: Add possibility to hide last activities for public
]
