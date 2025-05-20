from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

from django.template.loader import render_to_string

from server.apps.users.utils import get_email_verification_url


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

        # subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # # remove superfluous line breaks
        # subject = " ".join(subject.splitlines()).strip()
        # subject = self.format_email_subject(subject)

        template_name = f'{template_prefix}_message.html'
        body = render_to_string(template_name, context).strip()

        subject = context.get('subject', _('Mathlab | Notification'))
        msg = EmailMessage(subject, body, from_email, to, headers=headers)
        msg.content_subtype = 'html'  # Main content is now text/html

        return msg

    def get_email_confirmation_url(self, request, emailconfirmation):
        return get_email_verification_url(request, emailconfirmation)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.create_initial_theorist()

        return user
