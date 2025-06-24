from django.urls import path

from server.apps.theorist_notifications.logic.notifications import (
    NotificationsView,
    HXReadNotificationsView,
    HXUnreadNotificationsListView,
    HXDeletedNotificationsListView,
    LiveUnreadNotificationListView,
)
from server.apps.theorist_notifications.logic.notifications_management import (
    NotificationMarkAllReadView,
    NotificationDeleteView,
    NotificationMarkReadView,
    NotificationMarkAllDeletedView,
)

app_name = 'theorist_notifications'

urlpatterns = [
    path('all/', NotificationsView.as_view(), name='all'),
    path('hx-notifications-read/', HXReadNotificationsView.as_view(), name='hx-notifications-read'),
    path('hx-notifications-unread/', HXUnreadNotificationsListView.as_view(), name='hx-notifications-unread'),
    path('hx-notifications-deleted/', HXDeletedNotificationsListView.as_view(), name='hx-notifications-deleted'),
    path(
        'live-unread-notification-list/', LiveUnreadNotificationListView.as_view(), name='live_unread_notification_list'
    ),
    # Management urls
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='mark-all-read'),
    path('mark-all-deleted/', NotificationMarkAllDeletedView.as_view(), name='mark-all-deleted'),
    path('<uuid:uuid>/mark-read/', NotificationMarkReadView.as_view(), name='mark-read'),
    path('<uuid:uuid>/safe-delete/', NotificationDeleteView.as_view(), name='safe-delete'),
    # path('clear-all/', NotificationMarkAllReadView.as_view(), name='clear-all'),
]
