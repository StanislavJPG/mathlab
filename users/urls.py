from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from .views import *


urlpatterns = [
    path('login/', Login.as_view(), name='login_view'),
    path('logout/', Logout.as_view(), name='logout_view'),
    path('registration/', Register.as_view(), name='register_view'),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/drf-auth/', include('rest_framework.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
