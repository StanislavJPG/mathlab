from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView
from django_htmx.http import trigger_client_event

from server.apps.forum.forms.comments import CommentCreateForm, CommentUpdateForm
from server.apps.forum.models import Comment, Post
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class CommentCreateView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, CreateView):
    model = Comment
    template_name = 'comments/partials/comment_block_create.html'
    form_valid_message = _('Your comment has been added.')
    form_invalid_message = _('Error. Please, check your input and try again.')
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(uuid=self.kwargs['post_uuid'])
        return context

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                'post': Post.objects.get(uuid=self.kwargs['post_uuid']),
                'theorist': self.request.theorist,
            }
        )
        return kwargs

    def form_valid(self, form):
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        trigger_client_event(response, 'commentBlockChanged')
        return response


class CommentUpdateView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, UpdateView):
    model = Comment
    template_name = 'comments/partials/comment_block_update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_class = CommentUpdateForm
    form_valid_message = _('Your comment has been updated.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().filter(theorist=self.request.theorist)

    def form_valid(self, form):
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        trigger_client_event(response, 'commentBlockChanged')
        return response


class CommentDeleteView(LoginRequiredMixin, HXViewMixin, FormMessagesMixin, DeleteView):
    model = Comment
    template_name = 'posts/question_page.html'
    form_valid_message = _('Your comment has been deleted.')
    form_invalid_message = _('Error. Please, check your input and try again.')
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = HttpResponse()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        trigger_client_event(response, 'commentBlockChanged')
        return response
