from django.views.generic import DetailView
from django_filters.views import FilterView

from server.apps.game_area.filters import MathQuizPlayBlocksListFilter
from server.apps.game_area.models import MathQuiz, MathExpression, MathQuizScoreboard
from server.common.mixins.views import HXViewMixin


class MathQuizPlayBlocksListView(HXViewMixin, FilterView):
    model = MathQuiz
    filterset_class = MathQuizPlayBlocksListFilter
    template_name = 'quizzes/partials/quiz_block_list.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().order_by_difficulty()


class MathQuizBaseQuizView(DetailView):
    model = MathQuiz
    template_name = 'quizzes/base_quiz.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    context_object_name = 'quiz'


class MathQuizStartPlayView(HXViewMixin, DetailView):
    model = MathExpression
    template_name = 'quizzes/partials/quiz.html'
    context_object_name = 'expression'

    def get_queryset(self):
        return super().get_queryset().filter(math_quiz__uuid=self.kwargs['quiz_uuid'])

    def _get_progress_value(self, as_percentage):
        scoreboard = MathQuizScoreboard.objects.filter(
            solved_by=self.request.theorist
        ).first()  # TODO: Process for anonymousUser
        solved_expressions_count = scoreboard.solved_expressions.filter(
            math_quiz__uuid=self.kwargs['quiz_uuid']
        ).count()

        if as_percentage:
            return round((solved_expressions_count / self.get_object().math_quiz.math_expressions_count) * 100)
        else:
            return solved_expressions_count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_expression_pk = self.get_object().pk
        expressions_to_search = list(self.get_queryset().values_list('pk', flat=True))
        context['expression_pos'] = expressions_to_search.index(current_expression_pk) + 1
        context['step'] = self._get_progress_value(as_percentage=False)
        context['progress'] = self._get_progress_value(as_percentage=True)
        return context
