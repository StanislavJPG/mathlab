from django_filters.views import FilterView

from server.apps.game_area.filters import MathQuizPlayBlocksListFilter
from server.apps.game_area.models import MathQuiz
from server.common.mixins.views import HXViewMixin


class MathQuizPlayBlocksListView(HXViewMixin, FilterView):
    model = MathQuiz
    filterset_class = MathQuizPlayBlocksListFilter
    template_name = 'quizzes/partials/quiz_block_list.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().order_by_difficulty()
