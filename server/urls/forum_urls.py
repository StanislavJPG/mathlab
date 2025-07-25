from django.urls import path, include

app_name = 'forum'

urlpatterns = [
    path('', include('server.apps.forum.urls')),
    path('theorist/', include('server.apps.theorist.urls.forum_profile_urls')),
    path('mathlab-community/', include('server.apps.theorist_community.urls')),
    path('chat/', include('server.apps.theorist_chat.urls.urls')),
    path('theorist/notifications/', include('server.apps.theorist_notifications.urls')),
]
