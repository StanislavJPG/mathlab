from typing import Final

from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.models import Theorist


class CaptchaForm(forms.Form):
    captcha = CaptchaField(required=False)  # required arg will be changed while processing
    SESSION_ATTR_NAME = 'failed_attempts'
    SUCCESS_ATTR_NAME = 'success_attempts'
    _captcha_success_updated_flag = False

    HAS_CAPTCHA: Final[bool] = True  # for checking hasattr() purpose

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_captcha_field()

    @property
    def failed_attempts_count(self):
        return self._get_attempts()

    @property
    def success_attempts_count(self):
        return self._get_attempts(success=True)

    @property
    def is_captcha_valid(self):
        return self.failed_attempts_count >= 3 or self.success_attempts_count >= 6

    def _init_captcha_field(self):
        self.fields['captcha'].required = self.is_captcha_valid
        self.fields['captcha'].label = _('Captcha')

    def _get_session_key(self, success=False):
        return f'{self.SESSION_ATTR_NAME if not success else self.SUCCESS_ATTR_NAME}_{self.__class__.__name__.lower()}'

    def _get_attempts(self, success=False):
        return self.request.session.get(self._get_session_key(success), 0)

    def captcha_session_push(self):
        attempts = self._get_attempts()
        self.request.session[self._get_session_key()] = attempts + 1

    def captcha_success_try_session_push(self):
        if not self.request or self._captcha_success_updated_flag:
            return

        key = self._get_session_key(success=True)
        current = self._get_attempts(success=True)

        if not self.fields['captcha'].required:
            self.request.session[key] = current + 1
            self._captcha_success_updated_flag = True
        else:
            self.clean_form_success_attempts()

    def clean_form_fail_attempts(self):
        self.request.session.pop(self._get_session_key(), None)

    def clean_form_success_attempts(self):
        self.request.session.pop(self._get_session_key(success=True), None)


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
