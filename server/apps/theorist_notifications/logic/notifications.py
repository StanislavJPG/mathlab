from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, TemplateView
from notifications.helpers import get_notification_list

from server.apps.theorist_notifications.models import TheoristNotification
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'base_notifications.html'

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        noti_qs = TheoristNotification.objects.filter(theorist=self.request.theorist)
        context['deleted_notifications'] = noti_qs.deleted()
        context['read_notifications'] = noti_qs.read()
        context['unread_notifications'] = noti_qs.unread()
        return context


class HXReadNotificationsView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristNotification
    template_name = 'partials/notifications_list.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).read()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['htmx_target_block'] = 'notifications-read-js'
        return context


class HXUnreadNotificationsListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristNotification
    template_name = 'partials/notifications_list.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).unread()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['htmx_target_block'] = 'notifications-unread-js'
        return context


class HXDeletedNotificationsListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristNotification
    template_name = 'partials/notifications_list.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).deleted()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['htmx_target_block'] = 'notifications-deleted-js'
        return context


class LiveUnreadNotificationListView(View):
    def get(self, request, *args, **kwargs):
        """Return a json with a unread notification list"""
        try:
            user_is_authenticated = request.user.is_authenticated()
        except TypeError:  # Django >= 1.11
            user_is_authenticated = request.user.is_authenticated

        if not user_is_authenticated:
            data = {'unread_count': 0, 'unread_list': []}
            return JsonResponse(data)

        unread_list = get_notification_list(request, 'unread')
        notifications_dict = {str(x.id): x for x in request.user.notifications.all()}
        for item in unread_list:
            notification = notifications_dict.get(str(item.get('id')))
            if notification:
                item['uuid'] = str(notification.uuid)

        data = {'unread_count': request.user.notifications.unread().count(), 'unread_list': unread_list}
        return JsonResponse(data)
