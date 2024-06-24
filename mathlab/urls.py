from mathlab.views import page_not_found, server_error, unauthorized
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('explainme.urls'), name='explain me'),
    path('', include('solvexample.urls'), name='solve example'),
    path('', include('graphbuilder.urls'), name='graphs builder'),
    path('', include('users.urls'), name='users'),
    path('', include('forum.urls'), name='forum'),
    path('', include('math_news.urls'), name='math_news'),
    path('', include('chat.urls'), name='chat')
]

handler404 = page_not_found
handler500 = server_error
handler401 = unauthorized
