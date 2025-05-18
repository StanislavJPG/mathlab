from allauth.account.views import PasswordChangeView
from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import UpdateView, TemplateView, DetailView
from django.utils.translation import gettext_lazy as _
from django_htmx.http import HttpResponseClientRedirect

from server.apps.theorist.forms import TheoristProfileSettingsForm, TheoristProfileConfigurationsForm
from server.apps.theorist.models import TheoristProfileSettings, Theorist
from server.apps.users.forms import CustomPasswordChangeForm
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin, CaptchaViewMixin


class TheoristProfileSettingsGeneralView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/settings/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request: AuthenticatedHttpRequest
        context['theorist'] = self.request.theorist
        return context


class AbstractProfileSettingsFormView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, UpdateView):
    model = None
    form_class = None
    template_name = None
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully changed your profile data!')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_object(self, queryset=None):
        self.request: AuthenticatedHttpRequest
        return TheoristProfileSettings.objects.get(theorist=self.request.theorist)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theorist'] = self.request.theorist
        return context

    def form_valid(self, form):
        form.save()
        context = {**self.get_context_data(), 'form': form}
        block_form = render_to_string(self.template_name, context, request=self.request)
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponse(content=block_form)


class TheoristProfilePublicInfoFormView(CaptchaViewMixin, AbstractProfileSettingsFormView):
    model = Theorist
    template_name = 'profile/settings/partials/personal_info.html'
    form_class = TheoristProfileSettingsForm

    def get_object(self, queryset=None):
        self.request: AuthenticatedHttpRequest
        return Theorist.objects.get(uuid=self.request.theorist.uuid)


class TheoristProfileConfigurationsFormView(AbstractProfileSettingsFormView):
    model = TheoristProfileSettings
    form_class = TheoristProfileConfigurationsForm
    template_name = 'profile/settings/partials/configurations.html'


class TheoristProfilePasswordFormView(
    LoginRequiredMixin, FormMessagesMixin, HXViewMixin, CaptchaViewMixin, PasswordChangeView
):
    template_name = 'profile/settings/partials/password.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_class = CustomPasswordChangeForm
    form_valid_message = _('You successfully changed your password!')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        context['theorist'] = self.request.theorist
        return context

    def form_valid(self, form):
        form.clean_form_fail_attempts()
        form.save()

        context = {**self.get_context_data(), 'form': form}
        block_form = render_to_string(self.template_name, context, request=self.request)
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponse(content=block_form)


class TheoristProfileDeactivateAccountView(LoginRequiredMixin, FormMessagesMixin, DetailView):
    model = Theorist
    template_name = 'profile/settings/partials/personal_info.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully changed your profile data!')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_object(self, queryset=None):
        self.request: AuthenticatedHttpRequest
        return Theorist.objects.get(uuid=self.request.theorist.uuid)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deactivate()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponseClientRedirect(reverse('forum:base-forum-page'))
