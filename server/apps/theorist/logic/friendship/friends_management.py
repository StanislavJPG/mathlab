from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.views.generic import DeleteView, DetailView
from django_htmx.http import trigger_client_event, HttpResponseClientRedirect
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.mixins import NotificationFriendshipMixin
from server.apps.theorist.models import TheoristFriendship, Theorist
from server.common.mixins.views import HXViewMixin


class TheoristFriendshipCreateView(
    LoginRequiredMixin, FormMessagesMixin, HXViewMixin, NotificationFriendshipMixin, DetailView
):
    model = Theorist
    slug_url_kwarg = 'theorist_uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully created friendship request!')
    form_invalid_message = _('Error. Please, check your input and try again.')
    notification_display_name = _('has sent friendship request to you')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            friendship = TheoristFriendship.create_friendship_request(from_=self.request.theorist, to=self.object)
            self.messages.success(self.get_form_valid_message(), fail_silently=True)
            self.send_notify(object=friendship)
            if self.request.GET.get('reload_next'):
                return HttpResponseClientRedirect(self.object.get_absolute_url())

            response = HttpResponse(status=201)
            trigger_client_event(response, 'friendshipBlockChanged')
            return response
        except ValidationError as exc:
            self.messages.error(exc.messages, fail_silently=True)
            return HttpResponse()


class TheoristAcceptFriendshipView(
    LoginRequiredMixin, FormMessagesMixin, HXViewMixin, NotificationFriendshipMixin, DetailView
):
    model = TheoristFriendship
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully accepted friendship request!')
    form_invalid_message = _('Error. Please, check your input and try again.')
    notification_display_name = _('has accepted your friendship request!')

    def get_queryset(self):
        return super().get_queryset().filter(receiver=self.request.theorist)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accept_friendship_request()
        response = HttpResponse()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        self.send_notify()

        trigger_client_event(response, 'friendshipBlockChanged')
        return response


class TheoristRejectFriendshipView(
    LoginRequiredMixin, FormMessagesMixin, HXViewMixin, NotificationFriendshipMixin, DetailView
):
    model = TheoristFriendship
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully rejected friendship request')
    form_invalid_message = _('Error. Please, check your input and try again.')
    notification_display_name = _('has rejected your friendship request!')

    def get_queryset(self):
        return super().get_queryset().filter(receiver=self.request.theorist)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.reject_friendship_request()
        response = HttpResponse()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        self.send_notify()

        trigger_client_event(response, 'friendshipBlockChanged')
        return response


class TheoristBrokeUpFriendshipView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, DeleteView):
    model = TheoristFriendship
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully broke up friendship with %s 😢')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_queryset(self):
        return super().get_queryset().filter(Q(receiver=self.request.theorist) | Q(requester=self.request.theorist))

    def get_form_valid_message(self):
        self.object = self.get_object()
        is_current_pending = self.request.GET.get('is_pending', None)
        if is_current_pending:
            self.form_valid_message = force_str(_('You successfully canceled your friendship request to %s 😢'))

        theorist = (
            self.object.receiver if self.object.requester_id == self.request.theorist.id else self.object.requester
        )
        return force_str(self.form_valid_message % theorist.full_name)

    def get_success_url(self):
        return self.request.theorist.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        self.object.delete()
        response = HttpResponse()

        trigger_client_event(response, 'friendshipBlockChanged')
        return response
