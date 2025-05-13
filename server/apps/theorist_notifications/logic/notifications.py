from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from server.apps.theorist_notifications.models import TheoristNotification
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'base_notifications.html'

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        context['unread_notifications'] = TheoristNotification.objects.filter(theorist=self.request.theorist).unread()
        return context


class HXReadNotificationsView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristNotification
    template_name = 'partials/notifications_list.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).read()


class HXUnreadNotificationsListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristNotification
    template_name = 'partials/notifications_list.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).unread()
