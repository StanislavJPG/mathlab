from datetime import timedelta

from django.db.models import Q

from server.apps.game_area.models import MathQuizScoreboard


def get_solved_quizzes_uuids(request):
    if not request.user.is_authenticated:
        solved_quizzes_uuids = request.session.get('solved_quizzes', [])
    else:
        solved_quizzes_uuids = request.theorist.quiz_scoreboard.solved_quizzes.all().values_list('uuid', flat=True)
    return solved_quizzes_uuids


def _get_anonymous_progress(request, get_correct_solved_expressions):
    incorrect_solved_expressions = request.session.get('incorrect_solved_expr', [])
    solved_expressions = request.session.get('solved_expr', [])
    if get_correct_solved_expressions:
        return len(solved_expressions)

    return len(incorrect_solved_expressions + solved_expressions)


def _get_progress_value(request, math_quiz, as_percentage, get_correct_solved_expressions=False):
    theorist = getattr(request, 'theorist', None)

    if not theorist or not request.user.is_authenticated:
        solved_expressions_count = _get_anonymous_progress(
            request, get_correct_solved_expressions=get_correct_solved_expressions
        )
    else:
        add_expr = Q(mathsolvedexpressions__is_correct=True) if get_correct_solved_expressions else Q()
        scoreboard = MathQuizScoreboard.objects.filter(solved_by=theorist).first()
        solved_expressions_count = scoreboard.solved_expressions.filter(
            add_expr, math_quiz__uuid=math_quiz.uuid
        ).count()

    total_expressions = math_quiz.math_expressions_count
    return round((solved_expressions_count / total_expressions) * 100) if as_percentage else solved_expressions_count


def add_solved_quiz_for_anonymous_user(quiz_uuid: str, request):
    session = request.session
    solved_quizzes = session.get('solved_quizzes', [])  # stores uuids
    solved_quizzes.append(str(quiz_uuid))
    session['solved_quizzes'] = solved_quizzes
    session.modified = True
    return session


def get_quiz_time_left_for_anonymous_user(quiz_uuid, request):
    quizzes_with_additional = request.session.get('quizzes_with_additional', [])
    return (
        [timedelta(seconds=a.get('time_left')) for a in quizzes_with_additional if a.get('uuid') == quiz_uuid][0]
        if quizzes_with_additional
        else timedelta(0)
    )
