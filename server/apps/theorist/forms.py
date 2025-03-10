from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from server.apps.theorist.models import Theorist, TheoristProfileSettings


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


class TheoristProfileSettingsForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Username')}), required=False, max_length=150
    )
    about_me = forms.CharField(widget=forms.Textarea({'rows': 3}), required=False, max_length=150)
    country = CountryField().formfield()

    class Meta:
        model = TheoristProfileSettings
        fields = (
            'username',
            'about_me',
            'country',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theorist = self.instance.theorist
        self.fields['username'].initial = self.theorist.full_name
        self.fields['about_me'].initial = self.theorist.about_me
        self.fields['country'].initial = self.theorist.country

    def save(self, commit=True):
        settings = super().save(commit=False)
        if commit:
            settings.save()

        theorist = settings.theorist
        theorist.full_name = self.cleaned_data['username']
        theorist.about_me = self.cleaned_data['about_me']
        theorist.country = self.cleaned_data['country']
        theorist.save()

        return settings
