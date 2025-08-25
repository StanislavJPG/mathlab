from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from server.apps.game_area.filters import MathQuizPlayBlocksListFilter
from server.apps.game_area.models import MathQuiz, MathExpression, MathQuizScoreboard
from server.common.mixins.views import HXViewMixin


__all__ = ['MathQuizPlayBlocksListView', 'MathQuizBaseQuizView', 'MathQuizGameMenuView']


class MathQuizPlayBlocksListView(HXViewMixin, FilterView):
    model = MathQuiz
    filterset_class = MathQuizPlayBlocksListFilter
    template_name = 'quizzes/partials/quiz_block_list.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter_by_with_expressions().order_by_difficulty()


class MathQuizBaseQuizView(DetailView):
    model = MathQuiz
    template_name = 'quizzes/base_quiz.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    context_object_name = 'quiz'


class MathQuizGameMenuView(HXViewMixin, FormMixin, DetailView):
    model = MathExpression
    # form_class = MathQuizGameMenuForm
    template_name = 'quizzes/partials/quiz.html'
    context_object_name = 'expression'

    def get_queryset(self):
        return super().get_queryset().filter(math_quiz__uuid=self.kwargs['quiz_uuid'])

    def _get_anonymous_progress(self):
        quiz_uuid = str(self.kwargs['quiz_uuid'])
        solved_expressions = self.request.session.get(f'expr_for_quiz_{quiz_uuid}', [])
        return len(solved_expressions)  # TODO: Process saving expressions in session while saving by anonymous user!

    def _get_progress_value(self, as_percentage):
        theorist = getattr(self.request, 'theorist', None)

        if not theorist or not self.request.user.is_authenticated:
            solved_expressions_count = self._get_anonymous_progress()
        else:
            scoreboard = MathQuizScoreboard.objects.filter(solved_by=theorist).first()
            solved_expressions_count = scoreboard.solved_expressions.filter(
                math_quiz__uuid=self.kwargs['quiz_uuid']
            ).count()

        total_expressions = self.get_object().math_quiz.math_expressions_count
        return (
            round((solved_expressions_count / total_expressions) * 100) if as_percentage else solved_expressions_count
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_expression_pk = self.get_object().pk
        expressions_to_search = list(self.get_queryset().values_list('pk', flat=True))
        context['expression_pos'] = expressions_to_search.index(current_expression_pk) + 1
        context['step'] = self._get_progress_value(as_percentage=False)
        context['progress'] = self._get_progress_value(as_percentage=True)
        return context
