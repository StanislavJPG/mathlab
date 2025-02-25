from django.urls import path

from server.apps.theorist.logic.onboarding import TheoristOnboardingTemplateView, HXTheoristOnboardFormView

app_name = 'theorist_onboarding'

urlpatterns = [
    path('', TheoristOnboardingTemplateView.as_view(), name='base-page'),
    path(
        'form/<uuid:uuid>/',
        HXTheoristOnboardFormView.as_view(),
        name='hx-onboard-view',
    ),
]
