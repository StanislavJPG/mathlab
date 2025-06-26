from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from django_filters.views import FilterView
from render_block import render_block_to_string

from server.apps.theorist.models import Theorist
from server.common.mixins.views import HXViewMixin


class TheoristCommunityBaseTemplateView(TemplateView):
    template_name = 'base_community_list.html'


class HXTheoristCommunityBaseListView(HXViewMixin, FilterView):
    model = Theorist
    filterset_fields = ('full_name',)
    template_name = 'partials/theorist_community_base_list.html'
    context_object_name = 'theorists'
    paginate_by = 20

    def get_queryset(self):
        expressions = ~Q(uuid=self.request.theorist.uuid)
        expr_for_auth = expressions if self.request.user.is_authenticated else Q()

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
        expressions = ~Q(uuid=self.request.theorist.uuid)
        expr_for_auth = expressions if self.request.user.is_authenticated else Q()

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
