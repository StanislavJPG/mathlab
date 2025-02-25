from django import forms
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.models import Theorist


class TheoristOnboardForm(forms.ModelForm):
    class Meta:
        model = Theorist
        fields = ('country', 'social_media_url', 'website_url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['social_media_url'].widget.attrs['placeholder'] = _('Social media url (optional)')
        self.fields['website_url'].widget.attrs['placeholder'] = _('Website url (optional)')

    def save(self, commit=True):
        theorist = super().save(commit=False)
        theorist.apply_default_onboarding_data()
        theorist.save()
        return theorist
