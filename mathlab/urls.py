"""
URL configuration for mathlab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from mathlab.views import page_not_found, server_error, unauthorized
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import Login

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Swagger"
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('explainme.urls'), name='explain me'),
    path('', include('solvexample.urls'), name='solve example'),
    path('', include('graphbuilder.urls'), name='graphs builder'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('users.urls'), name='users'),
    path('', include('forum.urls'), name='forum'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = page_not_found
handler500 = server_error
handler401 = unauthorized
