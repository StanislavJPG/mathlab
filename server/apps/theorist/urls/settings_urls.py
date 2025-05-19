from django.urls import path

from server.apps.theorist.logic.profile_settings import (
    TheoristProfileSettingsGeneralView,
    TheoristProfilePublicInfoFormView,
    TheoristProfileConfigurationsFormView,
    TheoristProfileDeactivateAccountView,
    TheoristProfilePasswordFormView,
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
        name='hx-profile-public-info-form',
    ),
    path(
        'configurations/<uuid:uuid>/',
        TheoristProfileConfigurationsFormView.as_view(),
        name='hx-profile-configurations-form',
    ),
    path(
        'password/<uuid:uuid>/',
        TheoristProfilePasswordFormView.as_view(),
        name='hx-profile-password-form',
    ),
    path(
        'deactivate-account/<uuid:uuid>/',
        TheoristProfileDeactivateAccountView.as_view(),
        name='hx-profile-deactivate-account-form',
    ),
]
