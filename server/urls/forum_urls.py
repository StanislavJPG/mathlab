from django.urls import path, include

app_name = 'forum'

urlpatterns = [
    path('', include('server.apps.forum.urls.post_urls')),
    path('', include('server.apps.forum.urls.comment_urls')),
    path('theorist/', include('server.apps.theorist.urls.forum_profile_urls')),
    path('chat/', include('server.apps.theorist_chat.urls')),
]
