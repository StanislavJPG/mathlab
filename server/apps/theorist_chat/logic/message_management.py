from braces.views import FormInvalidMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.utils.translation import gettext_lazy as _


class InvalidChatMessageCreateView(LoginRequiredMixin, FormInvalidMessageMixin, View):
    form_invalid_message = _('Error. Message was not created because some of participants blocked another.')

    def get(self, request, *args, **kwargs):
        response = HttpResponse()
        self.messages.error(self.get_form_invalid_message(), fail_silently=True)
        return response
