from django.urls import path

from server.apps.users.logic.auths_actions import CustomLoginView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login-view'),
    # socialaccount
    # path('connections/', CustomGoogleSignupFormView.as_view(), name='custom-social-signup-view'),
]
