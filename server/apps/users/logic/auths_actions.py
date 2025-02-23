from allauth.account.views import LoginView, SignupView
from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView
from django_htmx.http import HttpResponseClientRedirect


class CustomBaseAuthenticationView(TemplateView):
    template_name = 'base_auth_site.html'


class CustomLoginView(LoginView):
    template_name = 'partials/login.html'

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('forum:post-list'))
        messages.success(self.request, 'Hurray!')
        return response


class CustomSignUpView(SignupView):
    template_name = 'partials/signup.html'
