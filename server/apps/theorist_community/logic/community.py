from datetime import timedelta

from django.db.models import Q, Value, CharField
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView, DetailView, ListView
from django_filters.views import FilterView
from render_block import render_block_to_string

from server.apps.theorist.models import Theorist
from server.apps.theorist_community.filters import TheoristCommunityFilter
from server.common.mixins.views import HXViewMixin


class TheoristCommunityBaseTemplateView(TemplateView):
    template_name = 'base_community_list.html'


class HXTheoristCommunityBaseListView(HXViewMixin, FilterView):
    model = Theorist
    filterset_class = TheoristCommunityFilter
    template_name = 'partials/theorist_community_base_list.html'
    context_object_name = 'theorists'
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_authenticated:
            expr_for_auth = ~Q(uuid=self.request.theorist.uuid)
        else:
            expr_for_auth = Q()

        return (
            super()
            .get_queryset()
            .filter(expr_for_auth, Q(user__is_active=True))
            .filter_by_is_onboarded()
            .order_by('-score')
        )


class HXTheoristCommunityFriendshipBlockView(HXViewMixin, DetailView):
    model = Theorist
    template_name = 'partials/theorist_community_base_list.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            expr_for_auth = ~Q(uuid=self.request.theorist.uuid)
        else:
            expr_for_auth = Q()

        return (
            super()
            .get_queryset()
            .filter(expr_for_auth, Q(user__is_active=True))
            .filter_by_is_onboarded()
            .order_by('-score')
        )

    def get(self, request, *args, **kwargs):
        block_to_render = render_block_to_string(
            template_name=self.template_name,
            block_name='friendship_block',
            context={
                'theorist': self.get_object(),
            },
            request=request,
        )
        return HttpResponse(content=block_to_render)


class TheoristFriendsLastActivitiesListView(HXViewMixin, ListView):
    model = Theorist
    template_name = 'partials/last_actions_block.html'
    paginate_by = 8
    context_object_name = 'activities_list'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            theorist = self.request.theorist
            friends = theorist.get_friends()
            qs = friends.prefetch_related('comments', 'posts', 'comment_likes_relations', 'post_likes_relations')
            activity = []

            three_days_ago = timezone.now() - timedelta(days=3)
            created_at_expr = Q(created_at__gte=three_days_ago)
            for obj in qs:
                posts = obj.posts.filter(created_at_expr).annotate(model_name=Value('post', output_field=CharField()))
                post_likes = obj.post_likes_relations.filter(created_at_expr).annotate(
                    model_name=Value('post_like', output_field=CharField())
                )
                comments = obj.comments.filter(created_at_expr).annotate(
                    model_name=Value('comment', output_field=CharField())
                )
                comment_likes = obj.comment_likes_relations.filter(created_at_expr).annotate(
                    model_name=Value('comment_like', output_field=CharField())
                )
                activity.extend(posts)
                activity.extend(post_likes)
                activity.extend(comments)
                activity.extend(comment_likes)

            # Sort by `created_at`
            return sorted(activity, key=lambda x: x.created_at, reverse=True)
        return Theorist.objects.none()
