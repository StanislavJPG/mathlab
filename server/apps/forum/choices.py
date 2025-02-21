from django.db import models
from django.utils.translation import gettext_lazy as _


class PostTypeChoices(models.TextChoices):
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
