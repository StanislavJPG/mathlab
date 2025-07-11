from django import forms
from django.utils.translation import gettext_lazy as _
from server.apps.complaints.models import Complaint


class ComplaintCreateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('complaint_text', 'category')

    def __init__(self, *args, **kwargs):
        self.object_for_co = kwargs.pop('object_for_co')
        self.is_rate_limited = kwargs.pop('is_rate_limited')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.is_rate_limited:
            self.add_error(None, _('🏁 Slow down! Too many requests! Wait a while...'))
        if not self.object_for_co:
            self.add_error(None, _('Invalid object to complaint.'))
        return cleaned_data

    def save(self, commit=False):
        commit = False  # keep it False to prevent ContentType errors
        instance = super().save(commit)
        instance.content_object = self.object_for_co
        instance.save()
