from urllib.parse import quote
from allauth.utils import build_absolute_uri

from allauth.account.forms import app_settings, LoginForm
from allauth.account.adapter import DefaultAccountAdapter, get_adapter
from allauth.account.forms import (
    ResetPasswordForm,
    default_token_generator,
)
from allauth.account.utils import user_username, user_pk_to_url_str
from django.conf import settings
from django.urls import reverse
from allauth.account.app_settings import LoginMethod
from allauth.account.internal import flows

from server.common.forms import CaptchaForm


class CustomLoginForm(CaptchaForm, LoginForm):
    pass


class CustomResetPasswordForm(ResetPasswordForm):
    def save(self, request, **kwargs) -> str:
        email = self.cleaned_data['email']
        if not self.users:
            flows.signup.send_unknown_account_mail(request, email)
            return email

        adapter: DefaultAccountAdapter = get_adapter()
        token_generator = kwargs.get('token_generator', default_token_generator)
        for user in self.users:
            temp_key = token_generator.make_token(user)

            # send the password reset email
            uid = user_pk_to_url_str(user)
            # We intentionally pass an opaque `key` on the interface here, and
            # not implementation details such as a separate `uidb36` and
            # `key. Ideally, this should have done on `urls` level as well.
            key = f'{uid}-{temp_key}'
            path = reverse('users:reset-password-key-view', kwargs={'uidb36': 'UID', 'key': 'KEY'})
            path = path.replace('UID-KEY', quote(key))
            url = build_absolute_uri(request, path)
            context = {
                'user': user,
                'password_reset_url': url,
                'uid': uid,
                'key': temp_key,
                'request': request,
                'operating_system': request.headers.get('Sec-Ch-Ua-Platform'),
                'browser_name': request.headers.get('User-Agent'),
                'default_site_url': build_absolute_uri(request, settings.SITE_DEFAULT_URL),
            }
            if LoginMethod.USERNAME in app_settings.LOGIN_METHODS:
                context['username'] = user_username(user)
            adapter.send_password_reset_mail(user, email, context)

        return email
