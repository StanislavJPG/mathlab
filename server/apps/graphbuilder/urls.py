from django.urls import path

from server.apps.graphbuilder.views.graphics import index

urlpatterns = [path("graphbuilder/", index, name="graphbuilder")]
