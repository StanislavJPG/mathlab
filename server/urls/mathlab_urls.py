from django.urls import path, include

app_name = 'mathlab'

urlpatterns = [
    path('', include('server.apps.explainme.urls'), name='explain me'),
    path('', include('server.apps.solvexample.urls'), name='solve example'),
    path('', include('server.apps.graphbuilder.urls'), name='graphs builder'),
    path('', include('server.apps.math_news.urls'), name='math_news'),
    # path('', include('server.apps.chat.urls'), name='chat'),
    path('', include('server.apps.carousel.urls'), name='carousel'),
]
