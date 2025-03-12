from captcha.fields import CaptchaField
from django import forms


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
