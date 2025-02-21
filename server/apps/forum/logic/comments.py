from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.http import HttpResponse

from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event
from render_block import render_block_to_string

from server.apps.forum.forms import CommentCreateForm
from server.apps.forum.models import Comment, Post
from server.common.http import AuthenticatedHttpRequest


__all__ = (
    'CommentListView',
    'CommentCreateView',
    'CommentDeleteView',
    'HXCommentQuantityView',
    'HXCommentLikesAndDislikesView',
)


class CommentListView(ListView):
    paginate_by = 7
    model = Comment
    context_object_name = 'comments'
    template_name = 'partials/comment_list.html'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        order_by = self._get_ordering_from_url()
        return (
            super()
            .get_queryset()
            .filter(post__uuid=self.kwargs['post_uuid'])
            .with_likes_counters()
            .with_have_rates_per_theorist(self.request.theorist.uuid)
            .order_by(order_by)
        )

    def _get_ordering_from_url(self):
        order_by = self.request.GET.get('order_by')
        kwargs = {'best': '-custom_likes_counter', 'newest': '-created_at'}
        return kwargs.get(order_by, 'created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(uuid=self.kwargs['post_uuid'])
        return context


class CommentCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    # TODO: check LoginRequiredMixin from braces or not
    model = Comment
    template_name = 'partials/comment_block_create.html'
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


class CommentDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    model = Comment
    template_name = 'question_page.html'
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


class HXCommentQuantityView(DetailView):
    model = Post
    template_name = 'question_page.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'post_uuid'

    def get(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        if not self.request.htmx:
            return HttpResponse(status=405)

        self.object = self.get_object()
        context = {'comment_quantity': self.object.comments.count()}

        rendered_block = render_block_to_string(
            self.template_name,
            'comment_quantity',
            context=context,
            request=self.request,
        )
        response = HttpResponse(content=rendered_block)
        return response


class HXCommentLikesAndDislikesView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'partials/comment_list.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .prefetch_related('likes', 'dislikes')
            .with_likes_counters()
            .with_have_rates_per_theorist(self.request.theorist.uuid)
        )

    def dispatch(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        if not self.request.htmx:
            return HttpResponse(status=405)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        self.object = self.get_object()

        context = {
            'comment': self.object,
        }

        rendered_block = render_block_to_string(
            self.template_name,
            'comment_likes_and_dislikes',
            context=context,
            request=self.request,
        )
        response = HttpResponse(content=rendered_block)
        return response

    def post(self, request, *args, **kwargs):
        request: AuthenticatedHttpRequest
        self.object = self.get_object()
        likes_manager = self.object.likes
        dislikes_manager = self.object.dislikes

        is_like = self.request.GET.get('like') == 'true'

        if is_like:
            if likes_manager.filter(uuid=request.theorist.uuid).exists():
                likes_manager.remove(request.theorist)
            else:
                dislikes_manager.remove(request.theorist)
                likes_manager.add(request.theorist)
        else:
            if dislikes_manager.filter(uuid=request.theorist.uuid).exists():
                dislikes_manager.remove(request.theorist)
            else:
                likes_manager.remove(request.theorist)
                dislikes_manager.add(request.theorist)

        response = HttpResponse()
        trigger_client_event(response, f'commentLikesAndDislikesChanged{self.object.uuid}')

        return response
