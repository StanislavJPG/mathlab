from django.urls import path, include

app_name = "forum"

urlpatterns = [
    path("", include("server.apps.forum.urls")),
]
