from braces.views import FormMessagesMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import is_ratelimited

from server.apps.complaints.forms import ComplaintCreateForm
from server.apps.complaints.models import Complaint
from server.apps.forum.models import Comment, Post
from server.apps.forum.models.comment import CommentAnswer
from server.apps.theorist.models import Theorist
from server.apps.theorist_chat.models import TheoristMessage
from server.apps.theorist_drafts.models import TheoristDrafts
from server.common.mixins.views import HXViewMixin


@method_decorator(ratelimit(key='ip', rate='5/m', group='complaint', method='POST', block=False), name='post')
class ComplaintCreateView(HXViewMixin, FormMessagesMixin, CreateView):
    model = Complaint
    template_name = 'modals/complaint_create_modal_form.html'
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
            'comment': (pgettext_lazy('2nd form', 'comment'), Comment),
            'comment-answer': (_('comment answer'), CommentAnswer),
            'post': (pgettext_lazy('2nd form', 'post'), Post),
            'message': (_('message'), TheoristMessage),
            'draft': (_('draft'), TheoristDrafts),
            'profile': (_('profile'), Theorist),
        }

    def get_object_from_kwargs(self):
        object_label = self.kwargs.get('object_label')
        object_uuid = self.kwargs.get('object_uuid')

        _map = self._map_of_accessed_models()
        model = _map.get(object_label, None)
        if model is not None:
            obj = model[1].objects.get(uuid=object_uuid)
            return obj

    def get_object_label_from_kwargs(self):
        object_label = self.kwargs.get('object_label')
        _map = self._map_of_accessed_models()
        model = _map.get(object_label, None)
        if model is not None:
            i18n = model[0]
            return i18n

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_rate_limited'] = is_ratelimited(
            self.request, rate='5/m', key='ip', method='POST', fn='complaint', group='complaint'
        )
        kwargs['object_for_co'] = self.get_object_from_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_label'] = self.get_object_label_from_kwargs()
        return context

    def form_valid(self, form):
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse(status=201)
        return response
