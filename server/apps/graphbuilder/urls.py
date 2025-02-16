from django.urls import path

from server.apps.graphbuilder.logic.graphics import index

urlpatterns = [path("graphbuilder/", index, name="graphbuilder")]
