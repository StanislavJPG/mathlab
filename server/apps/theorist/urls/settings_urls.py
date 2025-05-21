from django.urls import path

from server.apps.theorist.logic.profile_settings import (
    TheoristProfileSettingsGeneralView,
    TheoristProfilePersonalInfoFormView,
    TheoristProfileDeactivateAccountView,
    TheoristProfilePasswordFormView,
    TheoristProfileEmailConfigurationsFormView,
    TheoristProfileConfigurationsFormView,
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
        'personal-info/<uuid:uuid>/',
        TheoristProfilePersonalInfoFormView.as_view(),
        name='hx-profile-personal-info-form',
    ),
    path(
        'configurations/<uuid:uuid>/',
        TheoristProfileConfigurationsFormView.as_view(),
        name='hx-profile-configurations-form',
    ),
    path(
        'email/',
        TheoristProfileEmailConfigurationsFormView.as_view(),
        name='hx-profile-email-configurations-form',
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
