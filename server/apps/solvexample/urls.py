from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from server.apps.solvexample.views import equations, percents, matrix


urlpatterns = [
    path("solvexample/equations/", equations, name="equations"),
    path("solvexample/percents/", percents, name="percents"),
    path("solvexample/matrix/", matrix, name="matrices"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
