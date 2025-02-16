from django.urls import path

from server.apps.solvexample.logic.solvers import equations, percents, matrix


urlpatterns = [
    path("solvexample/equations/", equations, name="equations"),
    path("solvexample/percents/", percents, name="percents"),
    path("solvexample/matrix/", matrix, name="matrices"),
]
