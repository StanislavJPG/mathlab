from django.urls import path, include


urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('captcha/', include('captcha.urls')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
]
