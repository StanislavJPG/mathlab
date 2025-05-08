from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, CreateView, DetailView
from django_htmx.http import HttpResponseClientRedirect

from server.apps.theorist.models import Theorist, TheoristFriendship
from server.apps.theorist_chat.forms import MailBoxCreateForm
from server.apps.theorist_chat.mixins import ChatConfigurationRequiredMixin
from server.apps.theorist_chat.models import TheoristChatRoom
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class MailBoxCreateView(LoginRequiredMixin, ChatConfigurationRequiredMixin, FormMessagesMixin, HXViewMixin, CreateView):
    model = TheoristChatRoom
    template_name = 'modals/mailbox_create_modal.html'
    form_class = MailBoxCreateForm
    form_valid_message = _('You successfully created mailbox!')
    form_invalid_message = _('Some error happens. Please, try again later.')
    success_url = reverse_lazy('forum:theorist_chat:chat-base-page')

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(first_member__settings__is_able_to_get_messages=True)
                | Q(second_member__settings__is_able_to_get_messages=True)
            )
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        return kwargs

    def form_valid(self, form):
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponseClientRedirect(self.success_url)
        return response


class MailBoxCreateFromProfile(
    LoginRequiredMixin, ChatConfigurationRequiredMixin, FormMessagesMixin, HXViewMixin, DetailView
):
    model = Theorist
    slug_field = 'uuid'
    slug_url_kwarg = 'theorist_uuid'
    form_valid_message = _('You successfully created mailbox with %s!')
    form_invalid_message = _('It looks like chat with this theorists already exists.')

    def get_queryset(self):
        friendship_exists = (
            TheoristFriendship.objects.filter(
                (
                    Q(receiver__uuid=self.request.theorist.uuid, requester__uuid=self.kwargs['theorist_uuid'])
                    | Q(receiver__uuid=self.kwargs['theorist_uuid'], requester__uuid=self.request.theorist.uuid)
                )
            )
            .filter_by_accepted_status()
            .exists()
        )
        if friendship_exists:
            return (
                super()
                .get_queryset()
                .filter(
                    ~Q(id=self.request.theorist.id),
                    ~Q(blacklist__blocked_theorists=self.request.theorist),
                )
                .filter_is_able_to_get_messages()
            )
        return Theorist.objects.none()

    def get_form_valid_message(self):
        return force_str(self.form_valid_message % self.object.full_name)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        mailbox_form = MailBoxCreateForm(
            data={'second_member': self.object},
            theorist=self.request.theorist,
        )
        if mailbox_form.is_valid():
            mailbox_form.save()
            self.messages.success(self.get_form_valid_message(), fail_silently=True)
            response = HttpResponseClientRedirect(reverse('forum:theorist_chat:chat-base-page'))
        else:
            self.messages.error(self.get_form_invalid_message(), fail_silently=True)
            response = HttpResponse()
        return response


class MailBoxDeleteView(LoginRequiredMixin, ChatConfigurationRequiredMixin, FormMessagesMixin, HXViewMixin, DeleteView):
    model = TheoristChatRoom
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully deleted chat!')
    form_invalid_message = _('Some error happens. Please, try again later.')
    success_url = reverse_lazy('forum:theorist_chat:chat-base-page')

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .filter(
                Q(first_member=self.request.theorist) | Q(second_member=self.request.theorist),
            )
        )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponseClientRedirect(self.get_success_url())
