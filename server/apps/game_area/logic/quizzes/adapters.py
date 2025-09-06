from django.db.models import Q

from server.apps.game_area.models import MathMultipleChoiceTask, MathExpression
from server.apps.game_area.models.quizzes import MathSolvedExpressions
from server.apps.game_area.utils import _get_progress_value


class QuizAdapter:
    def __init__(self, expression_object, expression_queryset, request):
        self.object = expression_object
        self.queryset = expression_queryset
        self.request = request

    def is_last_expression_to_answer(self):
        obj = self.object
        math_quiz = obj.math_quiz
        scoreboard = self.get_current_task_scoreboard()
        solved_count = math_quiz.math_expressions.filter(uuid__in=scoreboard['all_expressions']).count()

        return not scoreboard['current_task_is_finished'] and solved_count == math_quiz.math_expressions_count - 1

    def get_current_task_scoreboard(self):
        obj = self.object
        expr_uuid = str(obj.uuid)
        theorist = getattr(self.request, 'theorist', None)

        if not theorist or not self.request.user.is_authenticated:
            session = self.request.session
            incorrect = session.get('incorrect_solved_expr', [])
            solved = session.get('solved_expr', [])
            additional = session.get('expressions_with_additional', [])
            all_expr = incorrect + solved

            return {
                'current_task_is_finished': expr_uuid in all_expr,
                'current_task_is_successfully_finished': expr_uuid in solved,
                'all_expressions': all_expr,
                'expression_answer': [a.get('answer') for a in additional if a.get('uuid') == expr_uuid]
                if additional
                else None,
            }

        scoreboard_qs = MathSolvedExpressions.objects.filter(
            math_expression=obj, math_quiz_scoreboard=theorist.quiz_scoreboard
        )

        scoreboard_entry = scoreboard_qs.first()
        return {
            'current_task_is_finished': scoreboard_qs.exists(),
            'current_task_is_successfully_finished': scoreboard_qs.filter(is_correct=True).exists(),
            'all_expressions': theorist.quiz_scoreboard.solved_expressions.values_list('uuid', flat=True),
            'expression_answer': getattr(scoreboard_entry, 'math_expression_answer', None),
        }

    def get_expression_stats(self, expressions):
        is_authenticated = self.request.user.is_authenticated
        if is_authenticated:
            stats = MathSolvedExpressions.objects.filter(
                math_quiz_scoreboard__solved_by=self.request.theorist
            ).values_list('math_expression__uuid', 'is_correct')

            solved = {uuid for uuid, correct in stats if correct}
            failed = {uuid for uuid, correct in stats if not correct}
        else:
            solved = set(self.request.session.get('solved_expr', []))
            failed = set(self.request.session.get('incorrect_solved_expr', []))

        return [
            {
                'pk': expr.pk,
                'uuid': expr.uuid,
                'is_solved': expr.uuid in solved if is_authenticated else str(expr.uuid) in solved,
                'is_solved_as_fail': expr.uuid in failed if is_authenticated else str(expr.uuid) in failed,
            }
            for expr in expressions
        ]

    def _get_navigation_pks(self, expressions, current_pk):
        try:
            idx = expressions.index(current_pk)
        except ValueError:
            return None, None

        prev_pk = expressions[idx - 1] if idx > 0 else None
        next_pk = expressions[idx + 1] if idx + 1 < len(expressions) else None
        return prev_pk, next_pk

    def _get_next_unsolved_pk(self, math_quiz, current_pk, solved_pks):
        return (
            MathExpression.objects.filter(
                ~Q(pk__in=solved_pks),
                ~Q(pk=current_pk),
                math_quiz=math_quiz,
            )
            .only('pk')
            .first()
        )

    def get_context_data(self, context):
        obj = self.object
        math_quiz = obj.math_quiz
        current_pk = obj.pk
        expressions = list(self.queryset)
        expression_pks = [expr.pk for expr in expressions]

        scoreboard = self.get_current_task_scoreboard()
        solved_exprs = math_quiz.math_expressions.filter(uuid__in=scoreboard['all_expressions'])
        solved_pks = list(solved_exprs.values_list('pk', flat=True))

        prev_pk, next_pk = self._get_navigation_pks(expression_pks, current_pk)
        next_unsolved = self._get_next_unsolved_pk(math_quiz, current_pk, solved_pks)

        context.update(
            {
                'expression_pos': expression_pks.index(current_pk) + 1,
                'progress_as_counter': _get_progress_value(self.request, math_quiz, as_percentage=False),
                'progress': _get_progress_value(self.request, math_quiz, as_percentage=True),
                'task': MathMultipleChoiceTask.objects.filter(math_expression=obj).first(),
                'is_last_expression_to_answer': self.is_last_expression_to_answer(),
                'expressions': self.get_expression_stats(expressions),
                'previous_task_pk': prev_pk,
                'next_task_pk': next_pk,
                'next_not_solved_task_pk': getattr(next_unsolved, 'pk', None),
                **scoreboard,
            }
        )

        return context
