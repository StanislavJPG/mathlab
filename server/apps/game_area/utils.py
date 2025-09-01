def get_solved_quizzes_uuids(request):
    if not request.user.is_authenticated:
        solved_quizzes_uuids = request.session.get('solved_quizzes', [])
    else:
        solved_quizzes_uuids = request.theorist.quiz_scoreboard.solved_quizzes.all().values_list('uuid', flat=True)
    return solved_quizzes_uuids
