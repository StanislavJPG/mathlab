from debug_toolbar.toolbar import debug_toolbar_urls

from django.contrib import admin
from django.urls import path, include

from server.common.http import base_redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", base_redirect, name="base-redirect"),
    # nested apps urls
    path("", include("server.apps.users.urls"), name="users"),
    path("mathlab/", include("server.urls.mathlab_urls")),
    path("forum/", include("server.urls.forum_urls")),
] + debug_toolbar_urls()
