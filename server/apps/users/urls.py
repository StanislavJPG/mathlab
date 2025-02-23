from django.urls import path

from server.apps.users.logic.auths_actions import CustomLoginView, CustomSignUpView, CustomBaseAuthenticationView

app_name = 'users'

urlpatterns = [
    path('join/', CustomBaseAuthenticationView.as_view(), name='base-auth'),
    path('login/', CustomLoginView.as_view(), name='login-view'),
    path('register/', CustomSignUpView.as_view(), name='register-view'),
    # socialaccount
]
