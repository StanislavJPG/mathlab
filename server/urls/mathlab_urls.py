from django.urls import path, include

app_name = 'mathlab'

urlpatterns = [
    path('', include('server.apps.solvers.urls'), name='solvers'),
    path('', include('server.apps.math_news.urls'), name='math_news'),
    path('', include('server.apps.carousel.urls'), name='carousel'),
    path('', include('server.apps.theorist_drafts.urls'), name='drafts'),
]
