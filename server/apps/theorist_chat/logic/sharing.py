from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django_htmx.http import HttpResponseClientRedirect

from server.apps.theorist_chat.forms import ShareViaMessageForm
from server.apps.theorist_drafts.models import TheoristDraftsConfiguration
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class AbstractMessageInstanceShareView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, CreateView):
    template_name = 'modals/messages_share_instance.html'
    form_class = ShareViaMessageForm
    success_url = None

    def _get_i18n_instance_name(self):
        raise NotImplementedError('Specify `_get_i18n_instance_name` method')

    def get_instance_to_share(self):
        raise NotImplementedError('Specify `get_instance_to_share` method')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['i18n_obj_name'] = self._get_i18n_instance_name()
        return context

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        kwargs['instance_uuid'] = self.kwargs['instance_uuid']
        kwargs['sharing_instance'] = self.get_instance_to_share()
        kwargs['i18n_obj_name'] = self._get_i18n_instance_name()
        return kwargs

    def get_form_valid_message(self):
        i18n_instance = self._get_i18n_instance_name()
        return force_str(_('You successfully shared %s.') % i18n_instance)

    def get_form_invalid_message(self):
        i18n_instance = self._get_i18n_instance_name()
        return force_str(_('Error while sharing %s. Please check for errors and try again.') % i18n_instance)

    def form_valid(self, form):
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponseClientRedirect(self.success_url)


class MessageDraftShareView(AbstractMessageInstanceShareView):
    success_url = reverse_lazy('mathlab:drafts:base-drafts')

    def get_instance_to_share(self):
        return TheoristDraftsConfiguration.objects.get(uuid=self.kwargs['instance_uuid'], is_public_available=True)

    def _get_i18n_instance_name(self):
        return _('my drafts')
