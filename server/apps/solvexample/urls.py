from django.urls import path

from server.apps.solvexample.logic.matrices import MatricesTemplateView
from server.apps.solvexample.logic.percents import PercentsTemplateView
from server.apps.solvexample.logic.equations import EquationsTemplateView
from server.apps.solvexample.logic import SolveTaskBaseView

urlpatterns = [
    path('solvexample/base/', SolveTaskBaseView.as_view(), name='solve-tasks-base'),
    path('solvexample/equations/', EquationsTemplateView.as_view(), name='equations'),
    path('solvexample/percents/', PercentsTemplateView.as_view(), name='percents'),
    path('solvexample/matrix/', MatricesTemplateView.as_view(), name='matrices'),
]
