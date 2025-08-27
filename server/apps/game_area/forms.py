from django import forms
from django.forms import HiddenInput

from server.apps.game_area.models import MathQuizScoreboard


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
        solved_expr_uuid = str(self.instance.uuid)
        solved = self.request.session.get('solved_expr', [])
        if solved_expr_uuid not in solved:
            solved.append(solved_expr_uuid)
            self.request.session['solved_expr'] = solved
            self.request.session.modified = True

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

                is_quiz_done = (
                    self.request.theorist.quiz_scoreboard.solved_expressions.filter(
                        math_quiz=self.instance.math_quiz
                    ).count()
                    >= self.instance.math_quiz.math_expressions.all().count()
                )
                print(is_quiz_done)
