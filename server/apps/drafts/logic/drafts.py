import base64

from braces.views import FormMessagesMixin
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView, CreateView
from django_htmx.http import HttpResponseClientRedirect

from server.apps.drafts.models import TheoristDrafts
from server.common.mixins.views import HXViewMixin


class TheoristDraftsBaseTemplateView(TemplateView):
    template_name = 'base_drafts.html'


class AbstractTheoristDraftsListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristDrafts
    context_object_name = 'drafts'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'


class TheoristDraftsAlbumListView(AbstractTheoristDraftsListView):
    template_name = 'partials/drafts_album_list.html'


class TheoristDraftsTableListView(AbstractTheoristDraftsListView):
    template_name = 'partials/drafts_album_list.html'


class TheoristDraftCreateForm(forms.ModelForm):
    draft = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = TheoristDrafts
        fields = ('label', 'draft', 'description')
        widgets = {
            'label': forms.TextInput(attrs={'placeholder': _('Draft label')}),
            'description': forms.Textarea(attrs={'placeholder': _('Description'), 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        super().__init__(*args, **kwargs)
        self.instance.theorist = self.theorist

    def clean_draft(self):
        draft = self.cleaned_data.get('draft')

        # Decode base64 image
        format, imgstr = draft.split(';base64,')
        ext = format.split('/')[-1]
        image_file = ContentFile(base64.b64decode(imgstr), name=f'drawing.{ext}')
        return image_file


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
