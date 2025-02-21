from django.urls import path
from django.contrib.auth import views as auth_views

from server.apps.users.logic.auths_actions import Login, Logout, Register, ResetPassword

urlpatterns = [
    path('login/', Login.as_view(), name='login_view'),
    path('logout/', Logout.as_view(), name='logout_view'),
    path('registration/', Register.as_view(), name='register_view'),
    path('password-reset/', ResetPassword.as_view(), name='password_reset'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='auth/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='auth/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
]
