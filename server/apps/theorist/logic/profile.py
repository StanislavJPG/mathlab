from itertools import chain

from django.contrib.auth.mixins import AccessMixin
from django.db.models import Value, CharField, Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView

from server.apps.theorist.choices import TheoristFriendshipStatusChoices
from server.apps.theorist.models import Theorist, TheoristFriendship, TheoristFriendshipBlackList
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin

__all__ = (
    'TheoristProfileDetailView',
    'HXTheoristDetailsProfileView',
    'TheoristLastActivitiesListView',
)


class TheoristProfileDetailView(AccessMixin, DetailView):
    model = Theorist
    template_name = 'profile/profile.html'
    context_object_name = 'theorist'
    raise_exception = True

    def get_queryset(self):
        return super().get_queryset().filter(is_onboarded=True)

    def dispatch(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        self.object = self.get_object()
        theorist = get_object_or_404(Theorist, pk=self.kwargs['pk'])
        valid_full_name_slug = theorist.full_name_slug
        if valid_full_name_slug != self.kwargs['full_name_slug']:
            return redirect(
                reverse(
                    'forum:theorist_profile:base-page',
                    kwargs={
                        'pk': self.kwargs['pk'],
                        'full_name_slug': valid_full_name_slug,
                    },
                )
            )
        if (
            self.object.settings.is_profile_only_for_authenticated and not request.user.is_authenticated
        ) or self.object.is_theorist_is_blocked(theorist=self.request.theorist):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request: AuthenticatedHttpRequest

        if self.request.user.is_authenticated:
            current_theorist = self.request.theorist
            target_theorist = self.get_object()

            friendship_qs = TheoristFriendship.objects.filter(
                Q(receiver=current_theorist, requester=target_theorist)
                | Q(receiver=target_theorist, requester=current_theorist)
            )

            context.update(
                {
                    'is_theorist_has_request': friendship_qs.filter(
                        receiver=current_theorist,
                        requester=target_theorist,
                        status=TheoristFriendshipStatusChoices.PENDING,
                    ).exists(),
                    'is_theorist_already_requested': friendship_qs.filter(
                        requester=current_theorist,
                        receiver=target_theorist,
                        status=TheoristFriendshipStatusChoices.PENDING,
                    ).exists(),
                    'is_theorists_are_friends': friendship_qs.filter(
                        status=TheoristFriendshipStatusChoices.ACCEPTED
                    ).exists(),
                    'is_theorists_are_rejected': friendship_qs.filter(
                        status=TheoristFriendshipStatusChoices.REJECTED
                    ).exists(),
                    'is_theorists_are_blocked': TheoristFriendshipBlackList.objects.filter(
                        owner=current_theorist, blocked_theorists=target_theorist
                    ).exists(),
                    'is_theorist_has_blocked': TheoristFriendshipBlackList.objects.filter(
                        owner=target_theorist, blocked_theorists=current_theorist
                    ).exists(),
                }
            )

        return context


class HXTheoristDetailsProfileView(HXViewMixin, DetailView):
    model = Theorist
    context_object_name = 'theorist'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().filter(full_name_slug=self.kwargs['full_name_slug'])

    def get_template_names(self):
        section = self.request.GET.get('section')
        if section == 'about-me':
            return 'profile/partials/about_me.html'
        elif section == 'statistics':
            return 'profile/partials/statistics.html'
        elif section == 'contact-info':
            return 'profile/partials/contact_info.html'


class TheoristLastActivitiesListView(ListView):
    model = Theorist
    template_name = 'profile/partials/last_activity.html'
    paginate_by = 5
    limit = 15  # custom attr to limit resulting activities
    context_object_name = 'activities_list'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .filter(uuid=self.kwargs['uuid'])
            .prefetch_related('comments', 'posts', 'comment_likes_relations', 'post_likes_relations')
        )
        obj = qs.get()

        posts = obj.posts.all().annotate(model_name=Value('post', output_field=CharField()))
        post_likes = obj.post_likes_relations.all().annotate(model_name=Value('post_like', output_field=CharField()))
        comments = obj.comments.all().annotate(model_name=Value('comment', output_field=CharField()))
        comment_likes = obj.comment_likes_relations.all().annotate(
            model_name=Value('comment_like', output_field=CharField())
        )

        combined_qs = chain(posts, post_likes, comments, comment_likes)

        # Sort by `created_at`
        return sorted(combined_qs, key=lambda x: x.created_at, reverse=True)[: self.limit]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['theorist'] = Theorist.objects.get(uuid=self.kwargs['uuid'])
        return context
