from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event

from server.apps.theorist_drafts.forms import TheoristDraftCreateForm, TheoristDraftUpdateForm, TheoristDraftUploadForm
from server.apps.theorist_drafts.models import TheoristDrafts
from server.common.mixins.views import HXViewMixin


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
        params = self.request.GET.get('view', 'album')
        return HttpResponseClientRedirect(form.get_absolute_url() + f'?view={params}')


class TheoristDraftUpdateView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, UpdateView):
    model = TheoristDrafts
    template_name = 'modals/edit_draft_modal.html'
    form_class = TheoristDraftUpdateForm
    form_valid_message = _('You successfully updated draft.')
    form_invalid_message = _('Error while updating draft. Please check for errors and try again.')
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        return kwargs

    def form_valid(self, form):
        form = form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        params = self.request.GET.get('view', 'album')
        return HttpResponseClientRedirect(form.get_absolute_url() + f'?view={params}')


class TheoristDraftUploadView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, CreateView):
    model = TheoristDrafts
    template_name = 'modals/upload_draft_modal.html'
    form_class = TheoristDraftUploadForm
    form_valid_message = _('You successfully uploaded draft.')
    form_invalid_message = _('Error while uploaded draft. Please check for errors and try again.')

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        return kwargs

    def form_valid(self, form):
        form = form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        params = self.request.GET.get('view', 'album')
        return HttpResponseClientRedirect(form.get_absolute_url() + f'?view={params}')


class TheoristDraftDeleteView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, DeleteView):
    model = TheoristDrafts
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully deleted draft.')
    form_invalid_message = _('Error while creating draft. Please check for errors and try again.')

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist)

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        trigger_client_event(response, 'draftDeleted')
        return response
