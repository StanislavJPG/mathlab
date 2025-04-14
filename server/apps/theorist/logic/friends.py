from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView

from server.apps.theorist.choices import TheoristFriendshipStatusChoices
from server.apps.theorist.models import TheoristFriendship
from server.common.mixins.views import HXViewMixin


class HXTheoristFriendshipListView(LoginRequiredMixin, HXViewMixin, ListView):  # may be FilterView
    model = TheoristFriendship
    template_name = 'profile/partials/friends_list.html'
    context_object_name = 'friends'
    paginate_by = 15
    raise_exception = False
    login_url = reverse_lazy('exception:hx-401')

    def get_queryset(self):
        uuid = self.kwargs['uuid']
        return (
            super()
            .get_queryset()
            .filter(
                (Q(requester__uuid=uuid) | Q(receiver__uuid=uuid)) & Q(status=TheoristFriendshipStatusChoices.ACCEPTED)
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends_counter'] = self.get_queryset().count()
        return context
