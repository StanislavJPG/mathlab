from debug_toolbar.toolbar import debug_toolbar_urls

from server.apps.mathlab.views import page_not_found, server_error, unauthorized
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include("server.apps.explainme.urls"), name="explain me"),
    path("", include("server.apps.solvexample.urls"), name="solve example"),
    path("", include("server.apps.graphbuilder.urls"), name="graphs builder"),
    path("", include("server.apps.users.urls"), name="users"),
    path("", include("server.apps.forum.urls"), name="forum"),
    path("", include("server.apps.math_news.urls"), name="math_news"),
    path("", include("server.apps.chat.urls"), name="chat"),
] + debug_toolbar_urls()

handler404 = page_not_found
handler500 = server_error
handler401 = unauthorized
