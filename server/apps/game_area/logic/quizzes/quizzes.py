from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import ModelFormMixin
from django_filters.views import FilterView

from server.apps.game_area.filters import MathQuizPlayBlocksListFilter
from server.apps.game_area.forms import MathQuizGameMenuForm
from server.apps.game_area.models import MathQuiz, MathExpression, MathQuizScoreboard, MathMultipleChoiceTask
from server.apps.game_area.models.quizzes import MathSolvedExpressions
from server.apps.game_area.utils import get_solved_quizzes_uuids
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


__all__ = ['MathQuizPlayBlocksListView', 'MathQuizBaseQuizView', 'MathQuizGameMenuView']


def _get_anonymous_progress(request, get_correct_solved_expressions=True):
    if get_correct_solved_expressions:
        solved_expressions = request.session.get('solved_expr', [])
        return len(solved_expressions)
    incorrect_solved_expressions = request.session.get('incorrect_solved_expr', [])
    return len(incorrect_solved_expressions)


def _get_progress_value(request, math_quiz, as_percentage):
    theorist = getattr(request, 'theorist', None)

    if not theorist or not request.user.is_authenticated:
        solved_expressions_count = _get_anonymous_progress(request)
    else:
        scoreboard = MathQuizScoreboard.objects.filter(solved_by=theorist).first()
        solved_expressions_count = scoreboard.solved_expressions.filter(math_quiz__uuid=math_quiz.uuid).count()

    total_expressions = math_quiz.math_expressions_count
    return round((solved_expressions_count / total_expressions) * 100) if as_percentage else solved_expressions_count


class MathQuizPlayBlocksListView(HXViewMixin, FilterView):
    model = MathQuiz
    filterset_class = MathQuizPlayBlocksListFilter
    template_name = 'quizzes/partials/quiz_block_list.html'
    context_object_name = 'quizzes'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter_by_with_expressions().order_by_difficulty()

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['solved_quizzes_uuids'] = get_solved_quizzes_uuids(self.request)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solved_quizzes_uuids'] = get_solved_quizzes_uuids(self.request)
        return context


class MathQuizBaseQuizView(DetailView):
    model = MathQuiz
    template_name = 'quizzes/base_quiz.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'
    context_object_name = 'quiz'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('next_finish_quiz', False):
            math_quiz = self.get_object()
            return HttpResponseRedirect(reverse('mathlab:gamearea:quizzes:mathquiz-base', args=[math_quiz.uuid]))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        if self.request.user.is_authenticated:
            is_quiz_finished = self.request.theorist.quiz_scoreboard.solved_quizzes.filter(
                uuid=self.object.uuid
            ).exists()
            scoreboard = MathQuizScoreboard.objects.get(solved_by=self.request.theorist)
            last_solved_expr = scoreboard.solved_expressions.all().last()
        else:
            quiz_uuid = str(self.object.uuid)
            is_quiz_finished = quiz_uuid in self.request.session.get('solved_quizzes', [])
            last_solved_expr = ...  # TODO: Fill

        context['last_solved_expr'] = last_solved_expr or self.object.math_expressions.first()
        context['is_quiz_finished'] = is_quiz_finished
        context['progress_as_counter'] = _get_progress_value(self.request, self.get_object(), as_percentage=False)
        return context


class MathQuizGameMenuView(HXViewMixin, ModelFormMixin, DetailView):
    model = MathExpression
    form_class = MathQuizGameMenuForm
    template_name = 'quizzes/partials/quiz.html'
    context_object_name = 'expression'

    def get_queryset(self):
        return super().get_queryset().filter(math_quiz__uuid=self.kwargs['quiz_uuid']).select_related('math_quiz')

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

    def _get_current_task_scoreboard(self):
        theorist = getattr(self.request, 'theorist', None)

        if not theorist or not self.request.user.is_authenticated:
            incorrect_solved_expr = self.request.session.get('incorrect_solved_expr', [])
            solved_expressions = self.request.session.get('solved_expr', [])
            expressions_with_additional = self.request.session.get('expressions_with_additional', [])
            all_expressions = incorrect_solved_expr + solved_expressions
            expr_uuid = str(self.get_object().uuid)

            return {
                'current_task_is_finished': expr_uuid in all_expressions,
                'current_task_is_successfully_finished': expr_uuid in solved_expressions,
                'all_expressions': all_expressions,
                'expression_answer': [
                    a.get('answer') for a in expressions_with_additional if a.get('uuid') == expr_uuid
                ]
                if expressions_with_additional
                else None,
            }

        scoreboard = MathSolvedExpressions.objects.filter(
            math_expression=self.get_object(), math_quiz_scoreboard=self.request.theorist.quiz_scoreboard
        )

        return {
            'current_task_is_finished': scoreboard.exists(),
            'current_task_is_successfully_finished': scoreboard.filter(is_correct=True).exists(),
            'all_expressions': self.request.theorist.quiz_scoreboard.solved_expressions.all().values_list(
                'uuid', flat=True
            ),
            'expression_answer': scoreboard.first().math_expression_answer
            if hasattr(scoreboard.first(), 'math_expression_answer')
            else None,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_expression_pk = self.get_object().pk
        math_quiz = self.get_object().math_quiz
        expressions_to_search = list(self.get_queryset().values_list('pk', flat=True))
        context.update(
            {
                'expression_pos': expressions_to_search.index(current_expression_pk) + 1,
                'progress_as_counter': _get_progress_value(self.request, math_quiz, as_percentage=False),
                'progress': _get_progress_value(self.request, math_quiz, as_percentage=True),
                'task': MathMultipleChoiceTask.objects.filter(math_expression=self.get_object()).first(),
            }
        )
        current_task_scoreboard = self._get_current_task_scoreboard()
        current_solved_math_expressions = math_quiz.math_expressions.filter(
            uuid__in=current_task_scoreboard['all_expressions']
        )
        context['is_last_expression_to_answer'] = (
            not current_task_scoreboard['current_task_is_finished']
            and current_solved_math_expressions.count() == math_quiz.math_expressions_count - 1
        )

        if self.request.user.is_authenticated:
            expr_for_stat = MathSolvedExpressions.objects.filter(
                math_quiz_scoreboard__solved_by=self.request.theorist
            ).values_list('math_expression__uuid', 'is_correct')
            solved_uuids = [expr[0] for expr in expr_for_stat if expr[1]]
            failed_expressions = [expr[0] for expr in expr_for_stat if not expr[1]]

            context['expressions'] = [
                {
                    'pk': obj.pk,
                    'uuid': obj.uuid,
                    'is_solved': obj.uuid in solved_uuids,
                    'is_solved_as_fail': obj.uuid in failed_expressions,
                }
                for obj in self.get_queryset()
            ]
        else:
            solved_expr = self.request.session.get('solved_expr', [])
            context['expressions'] = self.object.math_quiz.math_expressions.filter(uuid__in=solved_expr)

        try:
            next_task_pk = expressions_to_search[expressions_to_search.index(current_expression_pk) + 1]
        except IndexError:
            next_task_pk = None

        if expressions_to_search.index(current_expression_pk) - 1 >= 0:
            previous_task_pk = expressions_to_search[expressions_to_search.index(current_expression_pk) - 1]
        else:
            previous_task_pk = None

        try:
            next_not_solved_task_pk = (
                MathExpression.objects.filter(
                    ~Q(pk__in=current_solved_math_expressions.values_list('pk', flat=True)),
                    math_quiz=math_quiz,
                )
                .only('pk')
                .first()
                .pk
            )
        except AttributeError:
            next_not_solved_task_pk = None

        context['next_task_pk'] = next_task_pk
        context['previous_task_pk'] = previous_task_pk
        context['next_not_solved_task_pk'] = next_not_solved_task_pk
        context.update(self._get_current_task_scoreboard())
        return context
