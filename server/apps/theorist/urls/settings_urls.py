from django.urls import path

from server.apps.theorist.logic.profile_settings import (
    TheoristProfileSettingsGeneralView,
    TheoristProfilePublicInfoFormView,
    TheoristProfileYourDataFormView,
    TheoristProfileDeactivateAccountView,
)

app_name = 'settings'

urlpatterns = [
    # settings
    path(
        '',
        TheoristProfileSettingsGeneralView.as_view(),
        name='theorist-profile-settings',
    ),
    path(
        'public-info/<uuid:uuid>/',
        TheoristProfilePublicInfoFormView.as_view(),
        name='hx-profile-private-info-form',
    ),
    path(
        'your-data/<uuid:uuid>/',
        TheoristProfileYourDataFormView.as_view(),
        name='hx-profile-your-data-form',
    ),
    path(
        'deactivate-account/<uuid:uuid>/',
        TheoristProfileDeactivateAccountView.as_view(),
        name='hx-profile-deactivate-account-form',
    ),
]
