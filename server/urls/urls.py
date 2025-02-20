from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static

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
    path(
        "mathlab/", include("server.urls.mathlab_urls")
    ),  # this is the main app for math operations
    path("forum/", include("server.urls.forum_urls")),  # math forum
    path("", include("server.apps.users.urls")),  # for auth purposes
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
