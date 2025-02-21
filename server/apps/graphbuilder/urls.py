from django.urls import path

from server.apps.graphbuilder.logic.graphics import GraphBuilderTemplateView

urlpatterns = [path('graphbuilder/', GraphBuilderTemplateView.as_view(), name='graphbuilder')]
