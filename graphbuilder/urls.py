from django.urls import path
from .views import *


urlpatterns = [
    path('graphbuilder/', index, name='graphbuilder')

]
