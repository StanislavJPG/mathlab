from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView
from django_filters.views import FilterView
from render_block import render_block_to_string

from server.apps.theorist_chat.filters import MailBoxFilter
from server.apps.theorist_chat.models import TheoristChatRoom, TheoristMessage
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'


class MailBoxListView(LoginRequiredMixin, HXViewMixin, FilterView):
    model = TheoristChatRoom
    filterset_class = MailBoxFilter
    context_object_name = 'mailboxes'
    template_name = 'partials/mailbox_list.html'
    # paginate_by = 7

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .filter(Q(first_member=self.request.theorist) | Q(second_member=self.request.theorist))
        )

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['theorist'] = self.request.theorist
        return kwargs


class ChatMessagesListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristMessage
    template_name = 'partials/chat_messages_list.html'
    context_object_name = 'messages'
    # paginate_by = 5

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .filter(
                Q(room__uuid=self.kwargs['room_uuid']),
                Q(room__first_member=self.request.theorist) | Q(room__second_member=self.request.theorist),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_uuid'] = self.kwargs['room_uuid']

        room = TheoristChatRoom.objects.get(uuid=self.kwargs['room_uuid'])
        first_member = room.first_member
        second_member = room.second_member
        context['receiver'] = first_member if first_member != self.request.theorist else second_member
        return context


class HXMailBoxView(LoginRequiredMixin, HXViewMixin, View):
    template_name = 'partials/mailbox_list.html'

    def get(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        obj = TheoristChatRoom.objects.filter(
            Q(first_member=self.request.theorist) | Q(second_member=self.request.theorist)
        )

        context = {
            'mailboxes': obj,
        }

        rendered_block = render_block_to_string(
            self.template_name,
            'mailbox',
            context=context,
            request=self.request,
        )
        response = HttpResponse(content=rendered_block)
        return response
