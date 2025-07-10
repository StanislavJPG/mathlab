from django import forms
from server.apps.complaints.models import Complaint


class ComplaintCreateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('complaint_text', 'category')

    def __init__(self, *args, **kwargs):
        self.object_for_co = kwargs.pop('object_for_co')
        super().__init__(*args, **kwargs)

    def save(self, commit=False):
        commit = False  # keep it False to prevent ContentType errors
        instance = super().save(commit)
        instance.content_object = self.object_for_co
        instance.save()
