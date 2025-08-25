import django_filters as filters
from django.utils.translation import gettext_lazy as _

from server.apps.game_area.choices import MathQuizCategoryChoices, MathQuizDifficultyChoices
from server.apps.game_area.models import MathQuiz


finish_score_choices = (
    ('<=5', _('Less or equals 5')),
    ('5-10', '5-10'),
    ('10-15', '10-15'),
    ('15-20', '15-20'),
    ('>=20', _('Greater or equals 20')),
)  # TODO: Fix consistency as default values*


class MathQuizPlayBlocksListFilter(filters.FilterSet):
    finish_score_reward = filters.ChoiceFilter(choices=finish_score_choices, method='filter_by_finish_score_reward')
    categories = filters.MultipleChoiceFilter(
        choices=MathQuizCategoryChoices,
        field_name='category',
    )
    difficulties = filters.MultipleChoiceFilter(
        choices=MathQuizDifficultyChoices,
        field_name='difficulty',
    )

    class Meta:
        model = MathQuiz
        fields = ('categories', 'difficulties', 'finish_score_reward')

    def filter_by_finish_score_reward(self, queryset, name, value):
        if value == '<=5':
            return queryset.filter(finish_score_reward__lte=5)
        if value == '>=20':
            return queryset.filter(finish_score_reward__gte=20)
        if '-' in value:
            processed_value = value.split('-')
            return queryset.filter(
                finish_score_reward__gte=processed_value[0], finish_score_reward__lte=processed_value[1]
            )
