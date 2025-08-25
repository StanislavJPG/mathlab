from django.views.generic import DetailView

from server.apps.game_area.models import MathQuizScoreboard
from server.common.mixins.views import HXViewMixin


class MathQuizStartPlayView(HXViewMixin, DetailView):
    model = MathQuizScoreboard
    template_name = 'quizzes/base_quiz.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def post(self, request, *args, **kwargs):
        # add checking if user is not anonymous
        ...
