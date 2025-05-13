from django.urls import path

from server.apps.theorist_notifications.logic.notifications import (
    NotificationMarkAllReadView,
    NotificationsView,
    HXReadNotificationsView,
    HXUnreadNotificationsListView,
)

app_name = 'theorist_notifications'

urlpatterns = [
    path('all/', NotificationsView.as_view(), name='all'),
    path('hx-notifications-read/', HXReadNotificationsView.as_view(), name='hx-notifications-read'),
    path('hx-notifications-unread/', HXUnreadNotificationsListView.as_view(), name='hx-notifications-unread'),
    # Management urls
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='mark-all-read'),
    # path('clear-all/', NotificationMarkAllReadView.as_view(), name='clear-all'),
]
