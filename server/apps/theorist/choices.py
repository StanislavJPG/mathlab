from django.db import models
from django.utils.translation import gettext_lazy as _


class TheoristRankChoices(models.TextChoices):
    JUNIOR = 'junior', _('Junior mathematician')
    OLYMPIC = 'olympic', _('Olympic')
    TEACHER = 'teacher', _('Teacher of mathematics')
    GURU = 'guru', _('Guru of mathematics')
    MATH_LORD = 'math_lord', _('Lord of mathematics')
