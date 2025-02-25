from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField, Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django_htmx.http import trigger_client_event

from server.apps.theorist.models import Theorist
from server.common.http import AuthenticatedHttpRequest


__all__ = (
    'TheoristProfileDetailView',
    'HXTheoristDetailsProfileView',
    'TheoristLastActivitiesListView',
)

from server.common.mixins.views import RaiseScoreMixin


class TheoristProfileDetailView(DetailView):
    model = Theorist
    template_name = 'profile/profile.html'
    context_object_name = 'theorist'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().filter(full_name_slug=self.kwargs['full_name_slug'])

    def dispatch(self, request, *args, **kwargs):
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
        return super().dispatch(request, *args, **kwargs)


class HXTheoristDetailsProfileView(DetailView):
    model = Theorist
    context_object_name = 'theorist'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().filter(full_name_slug=self.kwargs['full_name_slug'])

    def get_template_names(self):
        section = self.kwargs.get('section')
        if section == 'about-me':
            return 'profile/partials/about_me.html'
        elif section == 'statistics':
            return 'profile/partials/statistics.html'
        elif section == 'contact-info':
            return 'profile/partials/contact_info.html'


class HXTheoristRaiseScoreUpdateView(LoginRequiredMixin, RaiseScoreMixin, DetailView):
    model = Theorist
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        # logically, theorist cannot say thanks to himself for score raising
        return super().get_queryset().filter(~Q(uuid=self.request.theorist.uuid))

    def post(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        self.object = self.get_object()
        self._relation_by_request_param()
        response = HttpResponse()
        trigger_client_event(response, 'commentBlockChanged')
        return response


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
