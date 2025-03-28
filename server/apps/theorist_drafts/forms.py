import base64

from django import forms
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

from server.apps.theorist_drafts.models import TheoristDrafts


class TheoristDraftCreateForm(forms.ModelForm):
    draft = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = TheoristDrafts
        fields = ('label', 'draft', 'description', 'is_public_available')
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


class TheoristDraftUpdateForm(forms.ModelForm):
    class Meta:
        model = TheoristDrafts
        fields = ('label', 'description', 'is_public_available')
        widgets = {
            'label': forms.TextInput(attrs={'placeholder': _('Draft label')}),
            'description': forms.Textarea(attrs={'placeholder': _('Description'), 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        super().__init__(*args, **kwargs)
        self.instance.theorist = self.theorist
