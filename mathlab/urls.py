from django.conf import settings
from django.conf.urls.static import static

from mathlab.views import page_not_found, server_error, unauthorized
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('explainme/', include('explainme.urls'), name='explain me'),
    path('solvexample/', include('solvexample.urls'), name='solve example'),
    path('graphbuilder/', include('graphbuilder.urls'), name='graphs builder'),
    path('users/', include('users.urls'), name='users'),
    path('forum/', include('forum.urls'), name='forum'),
    path('math_news/', include('math_news.urls'), name='math_news'),
    path('chat/', include('chat.urls'), name='chat')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = page_not_found
handler500 = server_error
handler401 = unauthorized
