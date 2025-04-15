from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import UpdateView, DeleteView, DetailView
from django_htmx.http import trigger_client_event, HttpResponseClientRedirect
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.models import TheoristFriendship, Theorist
from server.common.mixins.views import HXViewMixin


class TheoristFriendshipCreateView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, DetailView):
    model = Theorist
    slug_url_kwarg = 'theorist_uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully created friendship request!')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        TheoristFriendship.create_friendship_request(from_=self.request.theorist, to=self.object)
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponseClientRedirect(self.object.get_absolute_url())


class TheoristAcceptFriendshipView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, UpdateView):
    model = TheoristFriendship
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully accepted friendship request!')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.accept_friendship_request()
        response = HttpResponse(status=201)
        self.messages.success(self.get_form_valid_message(), fail_silently=True)

        trigger_client_event(response, 'pendingBlockChanged')
        return response


class TheoristRejectFriendshipStatusView(LoginRequiredMixin, HXViewMixin, UpdateView):
    pass


class TheoristRemoveFriendshipView(LoginRequiredMixin, HXViewMixin, DeleteView):
    pass
