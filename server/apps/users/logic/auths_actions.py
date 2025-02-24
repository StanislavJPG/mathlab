from allauth.account.views import LoginView, SignupView, LogoutView
from braces.views import FormMessagesMixin
from django.urls import reverse
from django.views.generic import TemplateView
from django_htmx.http import HttpResponseClientRedirect


class CustomBaseAuthenticationView(TemplateView):
    template_name = 'base_auth_site.html'


class CustomLoginView(FormMessagesMixin, LoginView):
    template_name = 'partials/login.html'
    form_valid_message = 'Your comment has been added.'
    form_invalid_message = 'Error. Please, check your input and try again.'

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('forum:post-list'))
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class CustomSignUpView(FormMessagesMixin, SignupView):
    template_name = 'partials/signup.html'
    form_valid_message = 'Your comment has been added.'
    form_invalid_message = 'Error. Please, check your input and try again.'

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('forum:post-list'))
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class CustomLogoutUpView(FormMessagesMixin, LogoutView):
    form_valid_message = 'Your comment has been added.'
    form_invalid_message = 'Error. Please, check your input and try again.'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return HttpResponseClientRedirect(reverse('forum:post-list'))  # for HTMX purposes
