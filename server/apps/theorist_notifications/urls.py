from django.urls import path

from server.apps.theorist_notifications.logic.notifications import NotificationMarkAllReadView

app_name = 'theorist_notifications'

urlpatterns = [
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='mark-all-read'),
    # path('clear-all/', NotificationMarkAllReadView.as_view(), name='clear-all'),
]
