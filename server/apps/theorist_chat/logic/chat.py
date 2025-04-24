from distutils.util import strtobool

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView
from django_filters.views import FilterView
from render_block import render_block_to_string

from server.apps.theorist_chat.constants import DEFAULT_MAILBOX_PAGINATION
from server.apps.theorist_chat.filters import MailBoxFilter
from server.apps.theorist_chat.forms import MessageMessageSingleForm
from server.apps.theorist_chat.mixins import ChatConfigurationRequiredMixin
from server.apps.theorist_chat.models import TheoristChatRoom, TheoristMessage
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class ChatView(LoginRequiredMixin, ChatConfigurationRequiredMixin, TemplateView):
    template_name = 'chat.html'


class MailBoxListView(LoginRequiredMixin, ChatConfigurationRequiredMixin, HXViewMixin, FilterView):
    model = TheoristChatRoom
    filterset_class = MailBoxFilter
    context_object_name = 'mailboxes'
    template_name = 'partials/mailbox_list.html'
    paginate_by = DEFAULT_MAILBOX_PAGINATION

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .filter(Q(first_member=self.request.theorist) | Q(second_member=self.request.theorist))
        ).order_by_last_sms_sent_relevancy()

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['theorist'] = self.request.theorist
        return kwargs


class ChatMessagesListView(LoginRequiredMixin, ChatConfigurationRequiredMixin, HXViewMixin, ListView):
    model = TheoristMessage
    template_name = 'partials/chat_messages_list.html'
    context_object_name = 'messages'
    paginate_by = 15

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

    def paginate_queryset(self, queryset, page_size):
        paginate_queryset = super().paginate_queryset(queryset, page_size)
        paginator = paginate_queryset[0]
        vanilla_qs = self.get_queryset()

        last_page = self.get_paginator(vanilla_qs, self.get_paginate_by(vanilla_qs)).num_pages
        page_kwarg = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or last_page

        # Use last page to paginate by ascending by scrolling on top
        page = paginator.page(page_kwarg)
        return paginator, page, page.object_list, page.has_other_pages()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_uuid'] = self.kwargs['room_uuid']

        room = (
            TheoristChatRoom.objects.filter(uuid=self.kwargs['room_uuid'])
            .select_related('first_member', 'second_member')
            .first()
        )
        first_member = room.first_member
        second_member = room.second_member
        context['receiver'] = first_member if first_member != self.request.theorist else second_member
        context['message_as_form'] = MessageMessageSingleForm()
        context['is_blocked_by_first_member'] = first_member.blacklist.blocked_theorists.filter(
            id=second_member.id
        ).exists()
        context['is_blocked_by_second_member'] = second_member.blacklist.blocked_theorists.filter(
            id=first_member.id
        ).exists()
        context['is_request_theorist_blocked_recipient'] = self.request.theorist.blacklist.blocked_theorists.filter(
            Q(id=first_member.id) | Q(id=second_member.id)
        ).exists()
        return context


class HXMailBoxView(LoginRequiredMixin, ChatConfigurationRequiredMixin, HXViewMixin, View):
    template_name = 'partials/mailbox_list.html'
    paginate_by = DEFAULT_MAILBOX_PAGINATION

    def get_paginate_by(self):
        return self.paginate_by

    def get(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        objs = TheoristChatRoom.objects.filter(
            (Q(first_member=self.request.theorist) | Q(second_member=self.request.theorist))
        ).order_by_last_sms_sent_relevancy()

        if strtobool(self.request.GET.get('show_blocked_chats')) is False:
            objs = objs.exclude(
                Q(first_member__blacklist__blocked_theorists=F('second_member'))
                | Q(second_member__blacklist__blocked_theorists=F('first_member'))
            )

        p_objs = Paginator(objs, self.get_paginate_by())
        page_param = self.request.GET.get('page') or 1

        context = {
            'mailboxes': p_objs.page(page_param).object_list,
            'room_uuid': self.kwargs['room_uuid'],
            'page_obj': p_objs.page(page_param),
        }

        rendered_block = render_block_to_string(
            self.template_name,
            'mailbox',
            context=context,
            request=self.request,
        )
        response = HttpResponse(content=rendered_block)
        return response
