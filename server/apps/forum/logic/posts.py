from braces.views import FormMessagesMixin, LoginRequiredMixin
from django.db.models import Q

from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, CreateView, DetailView, TemplateView
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event
from hitcount.views import HitCountDetailView
from render_block import render_block_to_string

from server.apps.forum.filters import PostListFilter
from server.apps.forum.forms import PostCreateForm
from server.apps.forum.models import Post, PostCategory
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import CacheMixin, AvatarDetailViewMixin, HXViewMixin

__all__ = (
    'BasePostTemplateView',
    'PostSupportUpdateView',
    'PostListView',
    'PostDetailView',
    'PostCreateView',
    'PostDeleteView',
    'HXPostLikesAndDislikesView',
    'PostDefaultImageView',
)


class BasePostTemplateView(TemplateView):
    template_name = 'base_articles.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PostCategory.objects.all()
        return context


class PostListView(FilterView):
    paginate_by = 10
    model = Post
    filterset_class = PostListFilter
    context_object_name = 'posts'
    template_name = 'partials/posts_list.html'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().with_likes_counters().order_by('-created_at')


class PostDetailView(HitCountDetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'question_page.html'
    count_hit = True

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .filter(slug=self.kwargs['slug'])
            .prefetch_related('comments', 'categories')
            .with_likes_counters()
            .with_have_rates_per_theorist(self.request.theorist)
        )

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context


class PostCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    model = Post
    template_name = 'create_question_page.html'
    form_class = PostCreateForm
    form_valid_message = _('You successfully created a new post.')
    form_invalid_message = _('Error while creating post. Please check for errors and try again.')

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        return kwargs

    def form_valid(self, form):
        post = form.save()
        response = HttpResponseRedirect(post.get_absolute_url())
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class PostDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    model = Post
    template_name = 'base/forum_base.html'
    form_valid_message = _('Your post has been deleted.')
    form_invalid_message = _('Error. Please, check your input and try again.')
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()

        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        trigger_client_event(response, 'postDeleted')
        return response


class HXPostLikesAndDislikesView(LoginRequiredMixin, HXViewMixin, DetailView):
    model = Post
    template_name = 'question_page.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

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
