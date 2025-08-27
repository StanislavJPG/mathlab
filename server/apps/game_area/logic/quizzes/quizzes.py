from django.views.generic import DetailView
from django.views.generic.edit import ModelFormMixin
from django_filters.views import FilterView

from server.apps.game_area.filters import MathQuizPlayBlocksListFilter
from server.apps.game_area.forms import MathQuizGameMenuForm
from server.apps.game_area.models import MathQuiz, MathExpression, MathQuizScoreboard, MathMultipleChoiceTask
from server.common.http import AuthenticatedHttpRequest
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

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        if self.request.user.is_authenticated:
            is_quiz_finished = self.request.theorist.quiz_scoreboard.solved_quizzes.filter(
                uuid=self.object.uuid
            ).exists()
        else:
            quiz_uuid = str(self.object.uuid)
            is_quiz_finished = quiz_uuid in self.request.session.get('solved_quizzes', [])

        context['is_quiz_finished'] = is_quiz_finished
        return context


class MathQuizGameMenuView(HXViewMixin, ModelFormMixin, DetailView):
    model = MathExpression
    form_class = MathQuizGameMenuForm
    template_name = 'quizzes/partials/quiz.html'
    context_object_name = 'expression'

    def get_queryset(self):
        return super().get_queryset().filter(math_quiz__uuid=self.kwargs['quiz_uuid'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return None

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def _get_anonymous_progress(self):
        solved_expressions = self.request.session.get('solved_expr', [])
        return len(solved_expressions)

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
        context['progress_as_counter'] = self._get_progress_value(as_percentage=False)
        context['progress'] = self._get_progress_value(as_percentage=True)
        context['task'] = MathMultipleChoiceTask.objects.filter(math_expression=self.get_object()).first()
        try:
            next_task_pk = expressions_to_search[expressions_to_search.index(current_expression_pk) + 1]
        except IndexError:
            next_task_pk = None
        context['next_task_pk'] = next_task_pk
        return context
