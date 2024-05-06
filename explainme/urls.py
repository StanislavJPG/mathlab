from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path('explainme/', explain_me, name='explainme')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
