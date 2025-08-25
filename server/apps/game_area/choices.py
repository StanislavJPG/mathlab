from django.db import models
from django.utils.translation import gettext_lazy as _


class MathQuizCategoryChoices(models.TextChoices):
    GRAPH_FUNCTIONS = 'GF', _('Graph Functions')
    MATRICES = 'MT', _('Matrices')
    EQUATIONS = 'RV', _('Equations')
    INEQUALITIES = 'NR', _('Inequalities')
    SYSTEMS = 'SM', _('Systems of Equations')
    HIGHER_MATH = 'VM', _('Higher Mathematics')
    PROBABILITY_THEORY = 'TY', _('Probability Theory')
    COMBINATORICS = 'KM', _('Combinatorics')
    DISCRETE_MATH = 'DM', _('Discrete Mathematics')
    ELEMENTARY_MATH = 'PM', _('Elementary Mathematics')
    PERCENTAGES = 'VD', _('Percentages')
    TRIGONOMETRY = 'TG', _('Trigonometry')
    GEOMETRY = 'GM', _('Geometry')
    STATISTICS = 'YS', _('Probability and Statistics')
    ALGORITHMS = 'AL', _('Algorithms')
    ALGEBRA = 'AG', _('Algebra')
    OTHER = 'IN', _('Other')
    MATH_FACTS = 'MF', _('Math Facts')


class MathQuizDifficultyChoices(models.TextChoices):
    EASY = 'ES', _('Easy')
    NORMAL = 'NL', _('Normal')
    HARD = 'HD', _('Hard')
    EXTRA_HARD = 'EX', _('Extra Hard')


class MathQuizScoreboardScoreChoices(models.TextChoices):
    EMPTY = 'EM', _('Empty')  # 0 solved expressions
    BRONZE = 'BZ', _('Bronze')  # 15+ solved expressions
    SILVER = 'SI', _('Silver')  # 40+ solved expressions
    GOLD = 'GO', _('Gold')  # 80+ solved expressions
    PLATINUM = 'PL', _('Platinum')  # # 200+ solved expressions
