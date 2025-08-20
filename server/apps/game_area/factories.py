import datetime

import factory
from factory import fuzzy

from server.apps.game_area.choices import MathQuizCategoryChoices, MathQuizDifficultyChoices


class MathQuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'game_area.MathQuiz'

    category = fuzzy.FuzzyChoice(MathQuizCategoryChoices.choices, getter=lambda x: x[0])
    difficulty = fuzzy.FuzzyChoice(MathQuizDifficultyChoices.choices, getter=lambda x: x[0])
    finish_score_reward = fuzzy.FuzzyInteger(low=15, high=100)

    max_time_to_solve = factory.LazyFunction(
        lambda: datetime.timedelta(
            hours=factory.Faker('random_int', min=1, max=24).evaluate(None, None, {'locale': 'uk_UA'})
        )
    )
