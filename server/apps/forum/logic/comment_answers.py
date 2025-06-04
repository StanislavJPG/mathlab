from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event

from server.apps.forum.forms.answers import CommentAnswerCreateForm
from server.apps.forum.models.comment import Comment, CommentAnswer
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class HXCommentAnswerDetailView(HXViewMixin, MultipleObjectMixin, DetailView):
    model = Comment
    context_object_name = 'answers'
    template_name = 'comments/answers/answer_list.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    paginate_by = 3

    def paginate_queryset(self, queryset, page_size):
        if self._show_all_objects():  # show all queryset when ?show=all param is passed
            return None, None, queryset, False  # keep paginate_queryset() return's pattern
        return super().paginate_queryset(queryset, page_size)

    def _show_all_objects(self):
        return self.request.GET.get('show') == 'all'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        original_qs = self.object.answers.all()
        context = super().get_context_data(object_list=original_qs, **kwargs)
        _, _, qs, _ = self.paginate_queryset(original_qs, page_size=self.paginate_by)
        context['limit_to_show_all'] = (original_qs.count() > self.paginate_by) and (qs.count() < original_qs.count())
        context['more_objects'] = original_qs.count() - self.paginate_by if context['limit_to_show_all'] else 0
        context['comment_able_to_get_answers'] = False
        return context


class CommentAnswerCreateView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, CreateView):
    model = Comment
    form_class = CommentAnswerCreateForm
    template_name = 'comments/answers/partials/answer_block_create.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'comment_uuid'
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
        trigger_client_event(response, 'answerBlockChanged')
        return response


class CommentAnswerDeleteView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, DeleteView):
    model = CommentAnswer
    template_name = 'comments/answers/answer_list.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_valid_message = _('Your answer has been deleted.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist)

    def get_success_url(self):
        return None

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        response = HttpResponse()
        trigger_client_event(response, 'answerBlockChanged')
        return response
