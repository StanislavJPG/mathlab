from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import Avg

from server.apps.game_area.models import MathQuizScoreboard, MathQuiz


@receiver(m2m_changed, sender=MathQuizScoreboard.solved_quizzes.through)
def update_mathquiz_avg_time(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        for quiz_id in pk_set:
            quiz = MathQuiz.objects.get(pk=quiz_id)
            scoreboards = MathQuizScoreboard.objects.filter(solved_quizzes=quiz)

            avg_time = scoreboards.aggregate(avg=Avg('time_taken'))['avg']

            quiz.average_solve_time_statistic = avg_time
            quiz.save(update_fields=['average_solve_time_statistic'])
