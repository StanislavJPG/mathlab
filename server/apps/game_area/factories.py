import datetime
import random

import factory
from factory import fuzzy
from faker import Faker
from faker.providers import BaseProvider

from server.apps.game_area.choices import MathQuizCategoryChoices, MathQuizDifficultyChoices


class MathQuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'game_area.MathQuiz'

    category = fuzzy.FuzzyChoice(MathQuizCategoryChoices.choices, getter=lambda x: x[0])
    difficulty = fuzzy.FuzzyChoice(MathQuizDifficultyChoices.choices, getter=lambda x: x[0])
    finish_score_reward = fuzzy.FuzzyInteger(low=15, high=100)

    max_time_to_solve = factory.LazyFunction(
        lambda: datetime.timedelta(
            hours=factory.Faker('random_int', min=0, max=0).evaluate(None, None, {'locale': 'uk_UA'})
        )
    )


class LatexProvider(BaseProvider):
    def math_expr(self):
        """Return a random LaTeX math expression"""
        variables = ['x', 'y', 'z', 'a', 'b', 'c', '\\alpha', '\\beta', '\\gamma']
        funcs = ['\\sin', '\\cos', '\\tan', '\\log', '\\ln', '\\sqrt']
        ops = ['+', '-', '\\times', '\\cdot', '/', '^']

        # pick random pieces
        v1 = random.choice(variables)
        v2 = random.choice(variables)
        func = random.choice(funcs)
        op = random.choice(ops)
        num = random.randint(1, 9)

        # build an expression
        templates = [
            f'{func}({v1}) {op} {v2}',
            f'{v1}^{num} {op} {v2}',
            f'\\frac{{{v1}}}{{{v2}}}',
            f'\\int {v1} \\, d{v2}',
            f'\\sum_{{i=1}}^{{{num}}} {v1}_i',
            f'\\lim_{{{v1}\\to {num}}} {func}({v1})',
        ]
        return random.choice(templates)


extended_fake = Faker()
extended_fake.add_provider(LatexProvider)


class MathExpressionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'game_area.MathExpression'

    latex_expression = factory.LazyFunction(lambda: extended_fake.math_expr())
    max_time_to_solve = factory.LazyFunction(
        lambda: datetime.timedelta(
            hours=factory.Faker('random_int', min=0.5, max=1).evaluate(None, None, {'locale': 'uk_UA'})
        )
    )
    math_quiz = factory.SubFactory(MathQuizFactory)
