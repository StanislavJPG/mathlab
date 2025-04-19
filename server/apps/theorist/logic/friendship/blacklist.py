from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.views.generic import UpdateView, ListView, DetailView
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event

from server.apps.theorist.models import TheoristFriendshipBlackList, Theorist, TheoristBlacklist
from server.common.mixins.views import HXViewMixin


class HXTheoristBlacklistView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristBlacklist
    template_name = 'friendship/blacklist/partials/blacklist.html'
    context_object_name = 'blacklist'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(blacklist__owner=self.request.theorist)


class TheoristUnblockFromBlacklistView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, UpdateView):
    model = TheoristFriendshipBlackList
    template_name = 'friendship/blacklist/partials/blacklist.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_valid_message = _('You successfully unblocked %s')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.theorist)

    def get_form_valid_message(self):
        self.object = self.get_object()
        theorist = Theorist.objects.filter(uuid=self.kwargs['theorist_uuid']).first()
        return force_str(self.form_valid_message % theorist.full_name)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        theorist_to_unblock = Theorist.objects.filter(uuid=self.kwargs['theorist_uuid']).first()
        self.object.unblock(theorist=theorist_to_unblock)
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        trigger_client_event(response, 'friendshipBlockChanged')
        return response


class TheoristBlockView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, DetailView):
    model = TheoristFriendshipBlackList
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_valid_message = _('You successfully blocked %s')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.theorist)

    def get_form_valid_message(self):
        self.object = self.get_object()
        theorist = Theorist.objects.filter(uuid=self.kwargs['theorist_uuid']).first()
        return force_str(self.form_valid_message % theorist.full_name)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        theorist_to_block = Theorist.objects.filter(uuid=self.kwargs['theorist_uuid']).first()
        self.object.block(theorist=theorist_to_block)
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        trigger_client_event(response, 'friendshipBlockChanged')
        return response
