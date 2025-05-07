from braces.views import FormInvalidMessageMixin, FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from server.apps.theorist_chat.models import TheoristMessage
from server.common.mixins.views import HXViewMixin


class ChatMessageSafeDeleteView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, DetailView):
    model = TheoristMessage
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'partials/chat_messages_list.html'
    form_valid_message = _('You successfully deleted this message!')
    form_invalid_message = _('Error. You cannot delete this message!')

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(room__first_member=self.request.theorist) | Q(room__second_member=self.request.theorist))
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.safe_delete(deleted_by=self.request.theorist)
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        return response


class InvalidChatMessageCreateView(LoginRequiredMixin, FormInvalidMessageMixin, View):
    form_invalid_message = _('Error. Message was not created because some of participants blocked another.')

    def get(self, request, *args, **kwargs):
        response = HttpResponse()
        self.messages.error(self.get_form_invalid_message(), fail_silently=True)
        return response
