from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView

from server.common.mixins.views import HXViewMixin


class TheoristFriendshipCreateView(LoginRequiredMixin, HXViewMixin, CreateView):
    pass


class TheoristAcceptFriendshipStatusView(LoginRequiredMixin, HXViewMixin, UpdateView):
    pass


class TheoristRejectFriendshipStatusView(LoginRequiredMixin, HXViewMixin, UpdateView):
    pass


class TheoristRemoveFriendshipView(LoginRequiredMixin, HXViewMixin, DeleteView):
    pass
