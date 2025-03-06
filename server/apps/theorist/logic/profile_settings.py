from braces.views import FormMessagesMixin
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import UpdateView, TemplateView
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.models import TheoristProfileSettings
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class TheoristProfileSettingsForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Username')}), required=False, max_length=150
    )

    class Meta:
        model = TheoristProfileSettings
        fields = ('username', 'is_show_last_activities', 'is_able_to_get_messages')


class TheoristProfileSettingsGeneralView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/settings/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request: AuthenticatedHttpRequest
        context['theorist'] = self.request.theorist
        return context


class TheoristProfileSettingsFormView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, UpdateView):
    model = TheoristProfileSettings
    form_class = TheoristProfileSettingsForm
    template_name = 'profile/settings/partials/profile_details.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully changed your profile data!')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_object(self, queryset=None):
        self.request: AuthenticatedHttpRequest
        return TheoristProfileSettings.objects.get(theorist=self.request.theorist)

    def form_valid(self, form):
        form.save()
        block_form = render_to_string(self.template_name, {'form': self.get_form()}, request=self.request)
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponse(content=block_form)
