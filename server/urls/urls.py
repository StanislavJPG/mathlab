from debug_toolbar.toolbar import debug_toolbar_urls

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("server.urls.third_party_urls")),
    path(
        "",
        RedirectView.as_view(pattern_name="mathlab:base-math-news"),
        name="base-redirect",
    ),
    # nested apps urls
    path("", include("server.apps.users.urls"), name="users"),
    path("mathlab/", include("server.urls.mathlab_urls")),
    path("forum/", include("server.urls.forum_urls")),
] + debug_toolbar_urls()
