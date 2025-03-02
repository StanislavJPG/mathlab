from django.urls import reverse
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from allauth.account.views import LoginView, SignupView, LogoutView, PasswordResetView, ConfirmEmailView, EmailView

from braces.views import FormMessagesMixin

from django_htmx.http import HttpResponseClientRedirect


class CustomBaseAuthenticationView(TemplateView):
    template_name = 'base_auth_site.html'


class CustomLoginView(FormMessagesMixin, LoginView):
    template_name = 'partials/login.html'
    form_valid_message = _('You have logged in successfully.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('forum:base-forum-page'))
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class CustomSignUpView(FormMessagesMixin, SignupView):
    template_name = 'partials/signup.html'
    form_valid_message = _('You have registered successfully.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('forum:base-forum-page'))
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class CustomLogoutUpView(FormMessagesMixin, LogoutView):
    form_valid_message = _('You are successfully logout.')
    form_invalid_message = _('Error. Please, check for errors existing and try again.')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return HttpResponseClientRedirect(reverse('forum:base-forum-page'))  # for HTMX purposes


class CustomPasswordResetView(FormMessagesMixin, PasswordResetView):
    template_name = 'partials/password_reset.html'
    form_valid_message = _('You have registered successfully.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('users:login'))
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class CustomEmailView(EmailView): ...


class CustomConfirmEmailView(ConfirmEmailView): ...
