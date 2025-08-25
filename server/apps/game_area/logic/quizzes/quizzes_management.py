from django.http import HttpResponse
from django.views.generic import DetailView

from server.apps.game_area.models import MathQuizScoreboard
from server.common.mixins.views import HXViewMixin


class MathQuizConfirmAnswerView(HXViewMixin, DetailView):
    model = MathQuizScoreboard
    template_name = 'quizzes/base_quiz.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def _process_not_auth_user(self):
        return HttpResponse()  # TODO: add if user is anonymous

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self._process_not_auth_user()

        ...

        return HttpResponse()
