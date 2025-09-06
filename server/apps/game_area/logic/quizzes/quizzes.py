from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import ModelFormMixin
from django_filters.views import FilterView

from server.apps.game_area.filters import MathQuizPlayBlocksListFilter
from server.apps.game_area.forms import MathQuizGameMenuForm
from server.apps.game_area.logic.quizzes.adapters import QuizAdapter
from server.apps.game_area.models import MathQuiz, MathExpression, MathQuizScoreboard
from server.apps.game_area.models.quizzes import MathSolvedQuizzes
from server.apps.game_area.utils import get_solved_quizzes_uuids, _get_progress_value
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
            try:
                quiz_best_time_taken = MathSolvedQuizzes.objects.get(
                    math_quiz=self.object, math_quiz_scoreboard=scoreboard
                ).best_time_taken
            except ObjectDoesNotExist:
                quiz_best_time_taken = timedelta(0)
        else:
            quiz_uuid = str(self.object.uuid)
            is_quiz_finished = quiz_uuid in self.request.session.get('solved_quizzes', [])
            quizzes_with_additional = self.request.session.get('quizzes_with_additional', [])
            last_solved_expr = ...  # TODO: Fill
            quiz_best_time_taken = (
                [timedelta(seconds=a.get('time_left')) for a in quizzes_with_additional if a.get('uuid') == quiz_uuid][
                    0
                ]
                if quizzes_with_additional
                else timedelta(0)
            )

        context['quiz_best_time_taken'] = quiz_best_time_taken
        context['last_solved_expr'] = last_solved_expr or self.object.math_expressions.first()
        context['is_quiz_finished'] = is_quiz_finished
        context['progress_as_counter'] = _get_progress_value(self.request, self.get_object(), as_percentage=False)
        context['progress_correct_answers_counter'] = _get_progress_value(
            self.request, self.get_object(), as_percentage=False, get_correct_solved_expressions=True
        )
        return context


class MathQuizGameMenuView(HXViewMixin, ModelFormMixin, DetailView):
    model = MathExpression
    form_class = MathQuizGameMenuForm
    quiz_adapter = QuizAdapter
    template_name = 'quizzes/partials/quiz.html'
    context_object_name = 'expression'

    def get_queryset(self):
        return super().get_queryset().filter(math_quiz__uuid=self.kwargs['quiz_uuid']).select_related('math_quiz')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['instance'] = self.get_object()
        adapter = self.get_adapter()
        kwargs['is_last_expression_to_answer'] = adapter.is_last_expression_to_answer()
        return kwargs

    def get_success_url(self):
        return None

    def get_adapter(self):
        return self.quiz_adapter(self.get_object(), self.get_queryset(), self.request)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        adapter = self.get_adapter()
        adapter.get_context_data(context)
        return context
