from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import base36_to_int
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from allauth.account.views import (
    LoginView,
    SignupView,
    LogoutView,
    PasswordResetView,
    PasswordResetFromKeyView,
    ConfirmEmailView,
)

from braces.views import FormMessagesMixin

from django_htmx.http import HttpResponseClientRedirect

from server.apps.users.forms import CustomLoginForm
from server.apps.users.models import CustomUser
from server.common.mixins.views import CaptchaViewMixin


class CustomBaseAuthenticationView(TemplateView):
    template_name = 'base_auth_site.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('forum:base-forum-page'))
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(FormMessagesMixin, CaptchaViewMixin, LoginView):
    template_name = 'partials/login.html'
    form_class = CustomLoginForm
    form_valid_message = _('You have logged in successfully.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def form_valid(self, form):
        self.captcha_process(form)
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('forum:base-forum-page'))
        return response


class CustomSignUpView(FormMessagesMixin, SignupView):
    template_name = 'partials/signup.html'
    form_valid_message = _('You have created your account successfully. Now finish the registration.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('forum:base-forum-page'))
        return response


class CustomLogoutUpView(FormMessagesMixin, LogoutView):
    form_valid_message = _('You are successfully logged out.')
    form_invalid_message = _('Error. Please, check for errors existing and try again.')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return HttpResponseClientRedirect(reverse('forum:base-forum-page'))  # for HTMX purposes


class CustomConfirmEmailView(FormMessagesMixin, ConfirmEmailView):
    template_name = 'partials/email_confirm.html'
    form_valid_message = _('You successfully confirmed your email address.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        response = HttpResponseClientRedirect(reverse('forum:base-forum-page'))
        return response


class CustomPasswordResetView(FormMessagesMixin, PasswordResetView):
    template_name = 'partials/password_reset.html'
    form_valid_message = _('Password reset instruction has sent to your email address.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('users:base-auth'))
        return response


class CustomPasswordResetFromKeyView(FormMessagesMixin, PasswordResetFromKeyView):
    template_name = 'partials/password_reset_key.html'
    form_valid_message = _('You have changed your password successfully. Now your can log in.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('users:base-auth'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uid = base36_to_int(self.kwargs['uidb36'])
        context['user_to_reset'] = CustomUser.objects.filter(pk=uid).first()
        return context
