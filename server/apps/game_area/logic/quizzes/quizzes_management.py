from django.views.generic import DetailView

from server.apps.game_area.models import MathQuiz
from server.common.mixins.views import HXViewMixin


class FinishQuizView(HXViewMixin, DetailView):
    model = MathQuiz
