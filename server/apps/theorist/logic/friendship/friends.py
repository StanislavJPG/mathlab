from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView

from server.apps.theorist.choices import TheoristFriendshipStatusChoices
from server.apps.theorist.models import TheoristFriendship
from server.common.mixins.views import HXViewMixin


class HXTheoristFriendshipTemplateView(LoginRequiredMixin, HXViewMixin, TemplateView):
    template_name = 'profile/partials/friends_list.html'
    raise_exception = False
    login_url = reverse_lazy('exception:hx-401')


class HXTheoristFriendshipListView(LoginRequiredMixin, HXViewMixin, ListView):  # may be FilterView
    model = TheoristFriendship
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


class HXTheoristPrivateCommunityListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristFriendship
    context_object_name = 'friends'
    paginate_by = 15

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
