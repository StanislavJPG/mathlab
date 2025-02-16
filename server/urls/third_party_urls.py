from django.conf import settings
from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("tinymce/", include("tinymce.urls")),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
