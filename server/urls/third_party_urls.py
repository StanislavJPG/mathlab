from django.urls import path, include


urlpatterns = [
    path("tinymce/", include("tinymce.urls")),
]
