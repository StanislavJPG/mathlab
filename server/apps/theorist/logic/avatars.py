from braces.views import FormMessagesMixin
from django.http import HttpResponse
from django.views.generic import UpdateView
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event

from server.apps.theorist.models import Theorist
from server.common.mixins.accesses import OnlyOwnerChangesMixin
from server.common.mixins.views import AvatarDetailViewMixin, CacheMixin

__all__ = (
    'TheoristDefaultProfileImageView',
    'TheoristAvatarUploadView',
    'TheoristAvatarDeleteView',
)


class TheoristDefaultProfileImageView(CacheMixin, AvatarDetailViewMixin):
    model = Theorist
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    unique_avatar_field = 'user__email'
    cache_timeout = 120


class TheoristAvatarUploadView(OnlyOwnerChangesMixin, FormMessagesMixin, UpdateView):
    model = Theorist
    template_name = 'profile/partials/main_information_block.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    fields = ('custom_avatar',)
    form_valid_message = _('You successfully uploaded your avatar.')
    form_invalid_message = _('Error. Please check for errors and try again.')

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponse()
        trigger_client_event(response, 'imageChanged')
        return response


class TheoristAvatarDeleteView(OnlyOwnerChangesMixin, FormMessagesMixin, UpdateView):
    model = Theorist
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    form_valid_message = _('You successfully deleted your avatar.')
    form_invalid_message = _('Error. Please check for errors and try again.')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = HttpResponse()
        self.object.drop_avatar_to_default()
        trigger_client_event(response, 'imageChanged')
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response
