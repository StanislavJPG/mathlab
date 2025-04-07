from captcha.fields import CaptchaField
from django import forms

from server.apps.theorist.models import Theorist


class CaptchaForm(forms.Form):
    captcha = CaptchaField(required=False)
    SESSION_ATTR_NAME = 'failed_attempts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_captcha_field()

    def _init_captcha_field(self):
        attempts = self._get_failed_attempts()
        self.fields['captcha'].required = attempts >= 3

    @property
    def _session_key(self):
        return f'{self.SESSION_ATTR_NAME}_{self.__class__.__name__.lower()}'

    def _get_failed_attempts(self):
        return self.request.session.get(self._session_key, 0)

    def captcha_session_push(self):
        self.request.session[self._session_key] = self._get_failed_attempts() + 1

    def clean_form_fail_attempts(self):
        self.request.session.pop(self._session_key, None)

    @property
    def failed_attempts_count(self):
        return self._get_failed_attempts()


class AbstractChoicesWithAvatarsWidget:
    def __init__(self, *args, model=Theorist, **kwargs):
        attrs = kwargs.pop('attrs', {})
        super().__init__(attrs, *args, **kwargs)
        self.model = model

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            obj = self.model.objects.filter(uuid=str(value)).first()
            img = obj.html_tag_avatar(size=[45, 45])
            # see more: https://jsfiddle.net/sharmamehu01/k7zq6shg/2/
            option['attrs']['data-content'] = f'{img} {label}'
        return option


class ChoicesWithAvatarsWidget(AbstractChoicesWithAvatarsWidget, forms.Select): ...


class MultipleChoicesWithAvatarsWidget(AbstractChoicesWithAvatarsWidget, forms.SelectMultiple): ...
