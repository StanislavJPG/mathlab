from django.views.generic import ListView

from server.apps.game_area.models import MathQuiz
from server.common.mixins.views import HXViewMixin


class MathQuizPlayBlocksListView(HXViewMixin, ListView):  # TODO: change to FilterView
    model = MathQuiz
    template_name = 'quizzes/partials/quiz_block_list.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter()
