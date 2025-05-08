from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django_filters.views import FilterView
from render_block import render_block_to_string

from server.apps.theorist.choices import TheoristFriendshipStatusChoices
from server.apps.theorist.filters import TheoristPrivateFriendshipFilter, TheoristPublicFriendshipFilter
from server.apps.theorist.models import TheoristFriendship, TheoristFriendshipBlackList
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class HXTheoristFriendshipTemplateView(LoginRequiredMixin, HXViewMixin, TemplateView):
    template_name = 'profile/partials/friends_list.html'
    raise_exception = False
    login_url = reverse_lazy('exception:hx-401')


class HXTheoristFriendshipListView(LoginRequiredMixin, HXViewMixin, FilterView):
    model = TheoristFriendship
    filterset_class = TheoristPublicFriendshipFilter
    context_object_name = 'friends'
    paginate_by = 15
    raise_exception = False
    login_url = reverse_lazy('exception:hx-401')

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.theorist.uuid != kwargs['uuid']
            and kwargs['status'] in [TheoristFriendshipStatusChoices.REJECTED, TheoristFriendshipStatusChoices.PENDING]
        ):
            return redirect(reverse_lazy('exception:hx-404'))
        return super().dispatch(request, *args, **kwargs)

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['theorist'] = self.request.theorist
        return kwargs

    def get_friendship_status(self):
        if self.kwargs['status'] in TheoristFriendshipStatusChoices.values:
            return self.kwargs['status']
        return TheoristFriendshipStatusChoices.ACCEPTED

    def get_template_names(self):
        friendship = self.get_friendship_status()
        if friendship == TheoristFriendshipStatusChoices.PENDING:
            return ['friendship/partials/public_lists/pending_list.html']
        elif friendship == TheoristFriendshipStatusChoices.REJECTED:
            return ['friendship/partials/public_lists/rejected_list.html']
        else:
            return ['friendship/partials/public_lists/accepted_list.html']

    def get_queryset(self):
        uuid = self.kwargs['uuid']
        status = self.get_friendship_status()
        if status == TheoristFriendshipStatusChoices.ACCEPTED:
            filter_query = Q(requester__uuid=uuid) | Q(receiver__uuid=uuid)
        else:
            filter_query = Q(requester__uuid=uuid)
        return super().get_queryset().filter(filter_query & Q(status=status))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends_counter'] = self.get_queryset().count()
        return context


class TheoristPrivateCommunityTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'friendship/community_list.html'

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        theorist_friendship_qs = TheoristFriendship.objects.filter(receiver=self.request.theorist)
        context['accepted_status_counter'] = theorist_friendship_qs.filter_by_accepted_status().count()
        context['rejected_counter_counter'] = theorist_friendship_qs.filter_by_rejected_status().count()
        context['pending_status_counter'] = theorist_friendship_qs.filter_by_pending_status().count()

        blacklist = TheoristFriendshipBlackList.objects.get(owner=self.request.theorist)
        context['blacklist_counter'] = blacklist.blocked_theorists.all().count()
        return context


class HXTheoristPrivateCommunityListView(LoginRequiredMixin, HXViewMixin, FilterView):
    model = TheoristFriendship
    filterset_class = TheoristPrivateFriendshipFilter
    context_object_name = 'friends'
    paginate_by = 15

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['theorist'] = self.request.theorist
        return kwargs

    def get_friendship_status(self):
        if self.kwargs['status'] in TheoristFriendshipStatusChoices.values:
            return self.kwargs['status']
        return TheoristFriendshipStatusChoices.ACCEPTED

    def get_template_names(self):
        friendship = self.get_friendship_status()
        if friendship == TheoristFriendshipStatusChoices.PENDING:
            return ['friendship/partials/private_lists/pending_list.html']
        elif friendship == TheoristFriendshipStatusChoices.REJECTED:
            return ['friendship/partials/private_lists/rejected_list.html']
        else:
            return ['friendship/partials/private_lists/accepted_list.html']

    def get_queryset(self):
        status = self.get_friendship_status()
        if status == TheoristFriendshipStatusChoices.ACCEPTED:
            filter_query = Q(requester=self.request.theorist) | Q(receiver=self.request.theorist)
        else:
            filter_query = Q(receiver=self.request.theorist)
        return super().get_queryset().filter(filter_query & Q(status=status))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends_counter'] = self.get_queryset().count()
        return context


class HXCommunityListCounters(LoginRequiredMixin, HXViewMixin, View):
    template_name = 'friendship/community_list.html'

    def get(self, request, *args, **kwargs):
        theorist_friendship_qs = TheoristFriendship.objects.filter(receiver=self.request.theorist)
        blacklist = TheoristFriendshipBlackList.objects.get(owner=self.request.theorist)
        context = {
            'blacklist_counter': blacklist.blocked_theorists.all().count(),
            'accepted_status_counter': theorist_friendship_qs.filter_by_accepted_status().count(),
            'rejected_counter_counter': theorist_friendship_qs.filter_by_rejected_status().count(),
            'pending_status_counter': theorist_friendship_qs.filter_by_pending_status().count(),
        }
        block_to_render = render_block_to_string(
            self.template_name, block_name='friendship_nav_counters', context=context, request=self.request
        )
        return HttpResponse(content=block_to_render)
