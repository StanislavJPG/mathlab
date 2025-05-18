from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from server.apps.theorist.models import Theorist, TheoristProfileSettings
from server.common.forms import CaptchaForm


class TheoristOnboardForm(forms.ModelForm):
    about_me = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), max_length=150, required=False)

    class Meta:
        model = Theorist
        fields = ('country', 'about_me', 'social_media_url', 'website_url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about_me'].widget.attrs['placeholder'] = _('Tell something about yourself... (optional)')
        self.fields['social_media_url'].widget.attrs['placeholder'] = _('Social media url (optional)')
        self.fields['website_url'].widget.attrs['placeholder'] = _('Website url (optional)')

    def save(self, commit=True):
        theorist = super().save(commit=False)
        theorist.apply_default_onboarding_data()
        theorist.save()
        return theorist


class TheoristProfileSettingsForm(CaptchaForm, forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(), required=False, max_length=150)
    country = CountryField().formfield()

    class Meta:
        model = Theorist
        fields = (
            'full_name',
            'about_me',
            'country',
            'social_media_url',
            'website_url',
            'captcha',
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.theorist = self.instance
        # for username field
        self.fields['full_name'].label = _('Username')
        self.fields['full_name'].widget.attrs['placeholder'] = _('Username')
        # for about_me fields
        self.fields['about_me'].label = _('About me')
        self.fields['about_me'].widget.attrs['placeholder'] = _('Example: Love to solve math problems and coding.')
        self.fields['about_me'].widget.attrs['rows'] = 3
        # for country field
        self.fields['country'].label = _('Country')
        # for social_media_url field
        self.fields['social_media_url'].label = _('Social media url')
        self.fields['social_media_url'].widget.attrs['placeholder'] = 'https://www.instagram.com'
        # for website_url field
        self.fields['website_url'].label = _('Website URL')
        self.fields['website_url'].widget.attrs['placeholder'] = 'https://docs.python.org/uk/'


class TheoristProfileConfigurationsForm(forms.ModelForm):
    class Meta:
        model = TheoristProfileSettings
        fields = (
            'is_profile_only_for_authenticated',
            'is_show_about_me',
            'is_show_last_activities',
            'is_able_to_get_messages',
            'is_able_to_receive_notifications',
        )
