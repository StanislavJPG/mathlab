from django.urls import path

from server.apps.solvers.logic.equations import EquationsTemplateView

urlpatterns = [path('solvexample/equations/', EquationsTemplateView.as_view(), name='equations')]
