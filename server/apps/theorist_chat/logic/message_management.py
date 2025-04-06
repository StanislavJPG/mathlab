from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_str
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _

from server.apps.forum.models import Post, Comment
from server.apps.theorist.models import Theorist
from server.apps.theorist_chat.forms import ShareViaMessageForm
from server.apps.theorist_chat.models import TheoristMessage
from server.apps.theorist_drafts.models import TheoristDrafts
from server.common.mixins.views import HXViewMixin, InstanceTranslationViewMixin


class MessageInstanceShareView(
    LoginRequiredMixin, HXViewMixin, FormMessagesMixin, InstanceTranslationViewMixin, CreateView
):
    model = TheoristMessage
    template_name = 'modals/messages_share_instance.html'
    form_class = ShareViaMessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.kwargs['instance']
        context['i18n_obj_name'] = self._get_i18n_instance_name(instance)
        return context

    def _get_model_by_instance_label(self, instance):
        models_map = {'draft': TheoristDrafts, 'post': Post, 'comment': Comment, 'profile': Theorist}
        models_map = models_map.get(instance) or None
        if not models_map:
            raise ImproperlyConfigured('Need to specify model in map and add `get_share_url` to it.')

        return models_map

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.kwargs['instance']
        kwargs['theorist'] = self.request.theorist
        kwargs['kwarg_instance'] = self.kwargs['instance']
        kwargs['i18n_obj_name'] = self._get_i18n_instance_name(instance)
        kwargs['model_instance_label'] = self._get_model_by_instance_label(instance)
        kwargs['instance_uuid'] = self.kwargs['instance_uuid']
        return kwargs

    def get_form_valid_message(self):
        instance = self.kwargs['instance']
        i18n_instance = self._get_i18n_instance_name(instance)
        return force_str(_('You successfully shared %s.') % i18n_instance)

    def get_form_invalid_message(self):
        instance = self.kwargs['instance']
        i18n_instance = self._get_i18n_instance_name(instance)
        return force_str(_('Error while sharing %s. Please check for errors and try again.') % i18n_instance)
