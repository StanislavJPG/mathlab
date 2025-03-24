from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView, CreateView
from django_htmx.http import HttpResponseClientRedirect

from server.apps.drafts.forms import TheoristDraftCreateForm
from server.apps.drafts.models import TheoristDrafts
from server.common.mixins.views import HXViewMixin


class TheoristDraftsBaseTemplateView(TemplateView):
    template_name = 'base_drafts.html'


class AbstractTheoristDraftsListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristDrafts
    context_object_name = 'drafts'
    slug_url_kwarg = 'uuid'
    slug_field = 'theorist__uuid'


class TheoristDraftsAlbumListView(AbstractTheoristDraftsListView):
    template_name = 'partials/drafts_album_list.html'


class TheoristDraftsTableListView(AbstractTheoristDraftsListView):
    template_name = 'partials/drafts_album_list.html'


class TheoristDraftCreateView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, CreateView):
    model = TheoristDrafts
    form_class = TheoristDraftCreateForm
    template_name = 'modals/create_draft_modal.html'
    form_valid_message = _('You successfully created a new draft.')
    form_invalid_message = _('Error while creating draft. Please check for errors and try again.')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        return kwargs

    def form_valid(self, form):
        form = form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponseClientRedirect(form.get_absolute_url())
