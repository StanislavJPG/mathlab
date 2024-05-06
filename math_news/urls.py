from django.urls import path
from .views import NewsView, base_redirect

urlpatterns = [
    path('', base_redirect, name='base-redirect'),
    path('news/math/', NewsView.as_view(), name='base-math-news'),

]
