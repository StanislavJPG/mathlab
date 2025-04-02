from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView, ListView

from server.apps.theorist_chat.models import TheoristChatRoom, TheoristMessage
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'


class MailBoxListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristChatRoom
    context_object_name = 'mailboxes'
    template_name = 'partials/mailbox_list.html'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .filter(Q(first_member=self.request.theorist) | Q(second_member=self.request.theorist))
        )


class ChatMessagesListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristMessage
    template_name = 'partials/chat_messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .filter(Q(room__first_member=self.request.theorist) | Q(room__second_member=self.request.theorist))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_uuid'] = self.kwargs['room_uuid']
        return context
