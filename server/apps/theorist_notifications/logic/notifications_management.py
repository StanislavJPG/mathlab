from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django_htmx.http import trigger_client_event
from render_block import render_block_to_string

from server.apps.theorist_notifications.models import TheoristNotification
from server.common.mixins.views import HXViewMixin


class NotificationMarkAllReadView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, View):
    form_valid_message = _('You successfully marked all notifications as read!')
    form_invalid_message = _('Error. Please, try again later.')

    def get_queryset(self):
        return TheoristNotification.objects.filter(theorist=self.request.theorist)

    def get_template_name(self):
        if self.request.POST.get('from_notify_page'):
            return 'base_notifications.html'
        else:
            return 'partials/forum/forum_navbar.html'

    def post(self, request, *args, **kwargs):
        notifications_qs = self.get_queryset()
        notifications_qs.unread().mark_all_as_read()
        block_to_render = render_block_to_string(
            self.get_template_name(),
            block_name='notification',
            context={
                'unread_notifications': notifications_qs.unread(),
                'deleted_notifications': notifications_qs.deleted(),
            },
            request=request,
        )
        response = HttpResponse(content=block_to_render)
        trigger_client_event(response, 'notificationChanged')
        if self.request.POST.get('from_notify_page'):
            self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class NotificationMarkAllDeletedView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, View):
    form_valid_message = _('You successfully deleted all notifications!')
    form_invalid_message = _('Error. Please, try again later.')

    def get_queryset(self):
        return TheoristNotification.objects.filter(theorist=self.request.theorist)

    def post(self, request, *args, **kwargs):
        notifications_qs = self.get_queryset()
        notifications_qs.mark_all_as_deleted()
        block_to_render = render_block_to_string(
            'base_notifications.html',
            block_name='notification',
            context={
                'unread_notifications': notifications_qs.unread(),
                'deleted_notifications': notifications_qs.deleted(),
            },
            request=request,
        )
        response = HttpResponse(content=block_to_render)
        trigger_client_event(response, 'notificationChanged')
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class NotificationMarkReadView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, DetailView):
    model = TheoristNotification
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'partials/notifications_list.html'
    form_valid_message = _('You successfully mark this notification as read.')
    form_invalid_message = _('Error. Please, try again later.')

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).unread()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.mark_as_read()
        response = HttpResponse()
        trigger_client_event(response, 'notificationChanged')
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response


class NotificationDeleteView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, DetailView):
    model = TheoristNotification
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'partials/notifications_list.html'
    form_valid_message = _('You successfully deleted notification.')
    form_invalid_message = _('Error. Please, try again later.')

    def get_queryset(self):
        return super().get_queryset().filter(theorist=self.request.theorist).active()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.safe_delete()
        response = HttpResponse()
        trigger_client_event(response, 'notificationChanged')
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response
