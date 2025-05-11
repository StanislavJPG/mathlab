from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View

from server.apps.theorist_notifications.models import TheoristNotification
from server.common.mixins.views import HXViewMixin


class NotificationMarkAllReadView(LoginRequiredMixin, HXViewMixin, View):
    model = TheoristNotification

    def get_queryset(self):
        return self.model.objects.filter(theorist=self.request.theorist)

    def post(self, request, *args, **kwargs):
        notifications_qs = self.get_queryset()
        notifications_qs.mark_all_as_read()
        return HttpResponse()
