from django.db import models
from django.db.models import Case, When

from server.apps.game_area.choices import MathQuizDifficultyChoices


class MathQuizQuerySet(models.QuerySet):
    def order_by_difficulty(self, easy_first=True):
        ordering_prefix = '-' if not easy_first else ''
        return self.alias(
            difficulty_ranking=Case(
                When(difficulty=MathQuizDifficultyChoices.EASY, then=0),
                When(difficulty=MathQuizDifficultyChoices.NORMAL, then=1),
                When(difficulty=MathQuizDifficultyChoices.HARD, then=2),
                When(difficulty=MathQuizDifficultyChoices.EXTRA_HARD, then=3),
                output_field=models.IntegerField(),
            ),
        ).order_by(f'{ordering_prefix}difficulty_ranking')
