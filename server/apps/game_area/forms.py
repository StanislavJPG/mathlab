from datetime import timedelta

from django import forms
from django.db import transaction
from django.forms import HiddenInput

from server.apps.game_area.models import MathQuizScoreboard, MathSolvedQuizzes


class MathQuizGameMenuForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.instance = kwargs.pop('instance')  # mathexpression obj
        super().__init__(*args, **kwargs)
        self.fields['answer'] = forms.CharField(widget=forms.Textarea)
        if self.instance.has_multiple_choices is True:
            self.fields['answer'].widget = HiddenInput()
        else:
            self.fields['answer'].widget.attrs = {'class': 'form-control'}

    def _process_not_auth_user(self):
        session = self.request.session
        solved_expr_uuid = str(self.instance.uuid)

        # Update solved expressions
        solved_expressions = set(session.get('solved_expr', []))
        if solved_expr_uuid not in solved_expressions:
            solved_expressions.add(solved_expr_uuid)
            session['solved_expr'] = list(solved_expressions)
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

    @transaction.atomic
    def save(self):
        answer = self.cleaned_data['answer']

        if self.instance.has_multiple_choices is True:
            is_answer_correct = self.instance.multiple_choices_quizzes.filter(
                answers__answer=answer, answers__is_correct_answer=True
            ).exists()
            if is_answer_correct:
                if not self.request.user.is_authenticated:
                    return self._process_not_auth_user()

                scoreboard = MathQuizScoreboard.objects.get(solved_by=self.request.theorist)
                scoreboard.solved_expressions.add(self.instance)
                # self.request.theorist.quiz_scoreboard.refresh_from_db()  # because .theorist is lazy method

                is_quiz_done = (
                    self.request.theorist.quiz_scoreboard.solved_expressions.filter(
                        math_quiz=self.instance.math_quiz
                    ).count()
                    >= self.instance.math_quiz.math_expressions.all().count()
                )
                if is_quiz_done:
                    MathSolvedQuizzes.objects.create(
                        math_quiz=self.instance.math_quiz,
                        math_quiz_scoreboard=scoreboard,
                        best_time_taken=timedelta(minutes=15),  # TODO: Replace this placeholder
                    )
                return scoreboard
