import django_filters as filters

from server.apps.theorist.choices import TheoristRankChoices
from server.apps.theorist.models import Theorist


class TheoristCommunityFilter(filters.FilterSet):
    full_name = filters.CharFilter(
        lookup_expr='icontains',
    )
    rank = filters.ChoiceFilter(
        choices=TheoristRankChoices.choices,
        field_name='rank',
    )

    class Meta:
        model = Theorist
        fields = (
            'full_name',
            'rank',
        )
