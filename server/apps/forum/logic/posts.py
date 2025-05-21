from urllib.parse import urlencode

from braces.views import LoginRequiredMixin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event
from hitcount.views import HitCountDetailView
from render_block import render_block_to_string

from server.apps.forum.filters import PostListFilter
from server.apps.forum.models import Post
from server.common.enums import bool_enum
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import CacheMixin, AvatarDetailViewMixin, HXViewMixin, RatedFormMessagesMixin

__all__ = (
    'BasePostTemplateView',
    'PostSupportUpdateView',
    'PostListView',
    'PostDetailView',
    'HXPostLikesAndDislikesView',
    'PostDefaultImageView',
)


class BasePostTemplateView(TemplateView):
    template_name = 'base_articles.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request_get'] = urlencode(self.request.GET, doseq=True)
        return context


class PostListView(FilterView):
    paginate_by = 10
    model = Post
    filterset_class = PostListFilter
    context_object_name = 'posts'
    template_name = 'posts/partials/posts_list.html'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().with_likes_counters().order_by('-created_at')


class PostDetailView(HitCountDetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/question_page.html'
    count_hit = True

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        valid_slug = post.slug
        if valid_slug != self.kwargs['slug']:
            return redirect(
                reverse(
                    'forum:post-details',
                    kwargs={
                        'pk': self.kwargs['pk'],
                        'slug': valid_slug,
                    },
                )
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .prefetch_related('comments', 'categories')
            .with_likes_counters()
            .with_have_rates_per_theorist(self.request.theorist)
        )

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['request_get'] = urlencode(self.request.GET, doseq=True)
        return context


class HXPostLikesAndDislikesView(LoginRequiredMixin, RatedFormMessagesMixin, HXViewMixin, DetailView):
    model = Post
    template_name = 'posts/question_page.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    form_valid_like_message = _('You liked this post.')
    form_valid_dislike_message = _('You disliked this post.')
    form_invalid_message = _('Error. Please, try again later.')

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().with_likes_counters().with_have_rates_per_theorist(self.request.theorist)

    def get(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        self.object = self.get_object()

        context = {'post': self.object}

        rendered_block = render_block_to_string(
            self.template_name,
            'post_likes_and_dislikes',
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
        trigger_client_event(response, 'postLikesAndDislikesChanged')

        return response


class PostSupportUpdateView(LoginRequiredMixin, DetailView):
    model = Post
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        # logically, theorist cannot say thanks to himself for score raising
        return super().get_queryset().filter(~Q(theorist=self.request.theorist))

    def post(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        self.object = self.get_object()

        if not self.object.supports.exists():
            self.object.supports.add(self.request.theorist)
            self.object.theorist.add_min_score()

        response = HttpResponse()
        trigger_client_event(response, 'postBlockChanged')
        return response


class PostDefaultImageView(CacheMixin, AvatarDetailViewMixin):
    model = Post
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    avatar_unique_field = 'slug'
    avatar_variant = 'marble'
    avatar_square = True
    cache_timeout = 120
