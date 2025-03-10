from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

from django.template.loader import render_to_string


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=True)
        if not commit:
            user.save()
        user.create_initial_theorist()

        return user

    def render_mail(self, template_prefix, email, context, headers=None):
        to = [email] if isinstance(email, str) else email
        from_email = self.get_from_email()

        template_name = 'email/password_reset_key_message.html'
        body = render_to_string(template_name, context).strip()

        msg = EmailMessage(_('Mathlab | Password reset'), body, from_email, to, headers=headers)
        msg.content_subtype = 'html'  # Main content is now text/html

        return msg


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.create_initial_theorist()

        return user
