from django.urls import path

from server.apps.solvers.logic.solvers import EquationsTemplateView, GraphBuilderTemplateView

urlpatterns = [
    path('solvexample/equations/', EquationsTemplateView.as_view(), name='equations'),
    path('solvexample/graphbuilder/', GraphBuilderTemplateView.as_view(), name='graphbuilder'),
]
