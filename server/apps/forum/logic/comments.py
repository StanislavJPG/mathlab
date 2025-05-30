from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from django.views.generic import DetailView, ListView
from django_htmx.http import trigger_client_event
from render_block import render_block_to_string

from server.apps.forum.constants import COMMENTS_LIST_PAGINATED_BY
from server.apps.forum.models import Comment, Post
from server.common.enums import bool_enum
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin, RatedFormMessagesMixin

__all__ = (
    'CommentListView',
    'HXCommentQuantityView',
    'HXCommentLikesAndDislikesView',
    'CommentSupportUpdateView',
)


class CommentListView(HXViewMixin, ListView):
    paginate_by = COMMENTS_LIST_PAGINATED_BY
    model = Comment
    context_object_name = 'comments'
    template_name = 'comments/partials/comment_list.html'
    page_custom_kwarg = 'comment_page'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        order_by = self._get_ordering_from_url()
        return (
            super()
            .get_queryset()
            .filter(post__uuid=self.kwargs['post_uuid'])
            .with_likes_counters()
            .with_have_rates_per_theorist(self.request.theorist)
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


class HXCommentQuantityView(HXViewMixin, DetailView):
    model = Post
    template_name = 'posts/question_page.html'
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


class HXCommentLikesAndDislikesView(LoginRequiredMixin, RatedFormMessagesMixin, HXViewMixin, DetailView):
    model = Comment
    template_name = 'comments/partials/comment_list.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    form_valid_like_message = _('You liked this comment.')
    form_valid_dislike_message = _('You disliked this comment.')
    form_invalid_message = _('Error. Please, try again later.')

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .prefetch_related('likes', 'dislikes')
            .with_likes_counters()
            .with_have_rates_per_theorist(self.request.theorist)
        )

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

        is_like = self.request.GET.get(self.e.LIKE.value) == bool_enum.TRUE.value

        if is_like:
            if likes_manager.filter(uuid=request.theorist.uuid).exists():
                likes_manager.remove(request.theorist)
            else:
                dislikes_manager.remove(request.theorist)
                likes_manager.add(request.theorist)
                self.messages.info(self.get_form_valid_like_message(), fail_silently=True)
        else:
            if dislikes_manager.filter(uuid=request.theorist.uuid).exists():
                dislikes_manager.remove(request.theorist)
            else:
                likes_manager.remove(request.theorist)
                dislikes_manager.add(request.theorist)
                self.messages.info(self.get_form_valid_dislike_message(), fail_silently=True)

        response = HttpResponse()
        trigger_client_event(response, f'commentLikesAndDislikesChanged{self.object.uuid}')

        return response


class CommentSupportUpdateView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, DetailView):
    model = Comment
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_valid_message = _('You successfully supported this comment.')
    form_invalid_message = _('Error. Please, try again later.')

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        # logically, theorist cannot say thanks to himself for score raising
        return super().get_queryset().filter(~Q(theorist=self.request.theorist))

    def post(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        self.object = self.get_object()

        if not self.object.supports.exists():
            self.object.supports.add(self.request.theorist)
            self.object.theorist.add_max_score()

        response = HttpResponse()
        trigger_client_event(response, 'commentBlockChanged')
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response
