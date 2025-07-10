from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _

from server.apps.complaints.forms import ComplaintCreateForm
from server.apps.complaints.models import Complaint
from server.apps.forum.models import Comment, Post
from server.apps.theorist.models import Theorist
from server.apps.theorist_chat.models import TheoristMessage
from server.apps.theorist_drafts.models import TheoristDrafts
from server.common.mixins.views import HXViewMixin


class ComplaintCreateView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, CreateView):
    model = Complaint
    template_name = 'modals/complaint_create_modal_details.html'
    form_class = ComplaintCreateForm
    slug_url_kwarg = 'object_uuid'
    slug_field = 'uuid'
    form_valid_message = _('Your complaint was successfully sent. Thank you!')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_success_url(self):
        return None

    @staticmethod
    def _map_of_accessed_models():
        return {
            'comment': Comment,
            'post': Post,
            'message': TheoristMessage,
            'draft': TheoristDrafts,
            'profile': Theorist,
        }

    def get_object_from_kwargs(self, object_label, object_uuid):
        _map = self._map_of_accessed_models()
        model = _map.get(object_label, None)

        if model is not None:
            obj = model.objects.get(uuid=object_uuid)
            return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        object_label = self.kwargs.get('object_label')
        object_uuid = self.kwargs.get('object_uuid')
        kwargs['object_for_ct'] = self.get_object_from_kwargs(object_label, object_uuid)
        return kwargs

    def form_valid(self, form):
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse(status=201)
        return response
