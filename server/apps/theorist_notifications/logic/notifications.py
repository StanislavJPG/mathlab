from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, TemplateView
from render_block import render_block_to_string

from server.apps.theorist_notifications.models import TheoristNotification
from server.common.mixins.views import HXViewMixin


class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'base_notifications.html'


class HXReadNotificationsView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristNotification
    template_name = 'partials/notifications_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).read()


class HXUnreadNotificationsListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristNotification
    template_name = 'partials/notifications_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).unread()


class NotificationMarkAllReadView(LoginRequiredMixin, HXViewMixin, View):
    model = TheoristNotification
    template_name = 'partials/forum/forum_navbar.html'

    def get_queryset(self):
        return self.model.objects.filter(theorist=self.request.theorist)

    def post(self, request, *args, **kwargs):
        notifications_qs = self.get_queryset()
        notifications_qs.mark_all_as_read()
        block_to_render = render_block_to_string(self.template_name, block_name='notification', request=request)
        return HttpResponse(content=block_to_render)
