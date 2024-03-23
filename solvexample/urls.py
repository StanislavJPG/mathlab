from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path('solvexample/', index),
    path('solvexample/percents', index)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
