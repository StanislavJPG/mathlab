from django import forms
from django.db import transaction
from django.forms import HiddenInput
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from server.apps.game_area.models import MathQuizScoreboard, MathSolvedQuizzes
from server.apps.game_area.models.quizzes import MathSolvedExpressions


class MathQuizGameMenuForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.is_last_expression_to_answer = kwargs.pop('is_last_expression_to_answer')
        self.instance = kwargs.pop('instance')  # mathexpression obj
        super().__init__(*args, **kwargs)
        # prepare answer field
        self.fields['answer'] = forms.CharField(widget=forms.Textarea)
        self.fields['answer'].widget = HiddenInput()
        self.fields['answer'].help_text = _('Write your answer below:')
        # prepare time_left field
        self.fields['time_left'] = forms.DurationField()
        self.fields['time_left'].widget = HiddenInput()
        self.fields['time_left'].required = False

        if self.is_last_expression_to_answer:
            self.fields['time_left'].required = True

    def _process_not_auth_user(self, is_correct_answer):
        session = self.request.session
        solved_expr_uuid = str(self.instance.uuid)
        solved_expressions = set(session.get('solved_expr', []))
        expressions_with_additional = session.get('expressions_with_additional', [])
        incorrect_solved_expressions = set()

        # Update solved expressions
        if is_correct_answer:
            solved_expressions.add(solved_expr_uuid)
            session['solved_expr'] = list(solved_expressions)
        else:
            incorrect_solved_expressions.add(solved_expr_uuid)
            session['incorrect_solved_expr'] = list(incorrect_solved_expressions)

        expressions_with_additional.append(
            {
                'uuid': solved_expr_uuid,
                'date': timezone.now().isoformat(),
                'answer': self.cleaned_data['answer'],
            }
        )
        session['expressions_with_additional'] = expressions_with_additional
        session.modified = True

        # Check if all expressions in the quiz are solved
        quiz = self.instance.math_quiz
        quiz_uuid = str(quiz.uuid)
        quiz_expression_uuids = set(quiz.math_expressions.values_list('uuid', flat=True))

        if quiz_expression_uuids.issubset(solved_expressions):
            solved_quizzes = set(session.get('solved_quizzes', []))
            if quiz_uuid not in solved_quizzes:
                solved_quizzes.add(quiz_uuid)
                session['solved_quizzes'] = list(solved_quizzes)
                session.modified = True

    def clean(self):
        already_solved_msg_label = _('Error. This expression is already solved.')

        if not self.request.user.is_authenticated:
            if str(self.instance.uuid) in self.request.session.get('solved_expr', []):
                self.add_error(None, already_solved_msg_label)
            return

        scoreboard = MathQuizScoreboard.objects.get(solved_by=self.request.theorist)
        if scoreboard.solved_expressions.filter(uuid=self.instance.uuid).exists():
            self.add_error(None, already_solved_msg_label)
            return

    @transaction.atomic
    def save(self):
        answer = self.cleaned_data['answer']

        if self.instance.has_multiple_choices is True:
            is_answer_correct = self.instance.multiple_choices_quizzes.filter(
                answers__answer=answer, answers__is_correct_answer=True
            ).exists()
        else:
            is_answer_correct = self.instance.compare_answer(answer)  # bool

        if not self.request.user.is_authenticated and not is_answer_correct:
            return self._process_not_auth_user(is_correct_answer=False)
        elif not self.request.user.is_authenticated and is_answer_correct:
            return self._process_not_auth_user(is_correct_answer=True)
        else:
            scoreboard = MathQuizScoreboard.objects.get(solved_by=self.request.theorist)

            solved_expr_dict = {
                'math_expression': self.instance,
                'math_quiz_scoreboard': scoreboard,
                'math_expression_answer': answer,
            }
            if is_answer_correct:
                solved_expr_dict['is_correct'] = True
                MathSolvedExpressions.objects.create(**solved_expr_dict)
            else:
                solved_expr_dict['is_correct'] = False
                MathSolvedExpressions.objects.create(**solved_expr_dict)

            solved_expressions = self.request.theorist.quiz_scoreboard.solved_expressions.filter(
                math_quiz=self.instance.math_quiz
            )

            is_quiz_done = solved_expressions.count() >= self.instance.math_quiz.math_expressions.all().count()
            if is_quiz_done:
                is_successfully_finished = (
                    solved_expressions.filter(mathsolvedexpressions__is_correct=True).count()
                    >= self.instance.math_quiz.min_expressions_to_successfully_finish
                )
                MathSolvedQuizzes.objects.create(
                    math_quiz=self.instance.math_quiz,
                    math_quiz_scoreboard=scoreboard,
                    best_time_taken=self.cleaned_data['time_left'],
                    is_successfully_finished=is_successfully_finished,
                )
            return scoreboard
