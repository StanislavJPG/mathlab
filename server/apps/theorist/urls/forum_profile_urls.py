from django.urls import path

from server.apps.theorist.logic.profile import (
    TheoristProfileDetailView,
    HXTheoristDetailsProfileView,
    TheoristLastActivitiesListView,
    HXTheoristRaiseScoreUpdateView,
)
from server.common.utils.redirects import theorist_email_verification_redirect_view

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
        '<uuid:uuid>/<uuid:model_uuid>/raise-score/<str:model>/',
        HXTheoristRaiseScoreUpdateView.as_view(),
        name='hx-theorist-raise-score',
    ),
    path(
        '<int:pk>/<slug:full_name_slug>/email-verification/redirect/',
        theorist_email_verification_redirect_view,
        name='email-verification-redirect',
    ),
    # path(
    #     'settings/<uuid:uuid>/',
    #     TheoristSettingsDetailView.as_view(),
    #     name='theorist-settings',
    # ),  # TODO: Add possibility to hide last activities for public
]
