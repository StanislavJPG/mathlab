from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView
from django.views.generic.list import MultipleObjectMixin
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event

from server.apps.forum.forms.answers import CommentAnswerCreateForm
from server.apps.forum.models.comment import Comment
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class HXCommentAnswerDetailView(HXViewMixin, MultipleObjectMixin, DetailView):
    model = Comment
    context_object_name = 'answers'
    template_name = 'comments/answers/answer_list.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        object_list = self.object.answers.all()
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class CommentAnswerCreateView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, CreateView):
    model = Comment
    form_class = CommentAnswerCreateForm
    template_name = 'comments/answers/partials/answer_block_create.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_valid_message = _('Your answer has been added.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        kwargs['comment'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        return context

    def form_valid(self, form):
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        trigger_client_event(response, 'commentBlockChanged')
        return response
