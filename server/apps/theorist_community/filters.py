import django_filters as filters
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.choices import TheoristRankChoices
from server.apps.theorist.models import Theorist


class TheoristCommunityFilter(filters.FilterSet):
    full_name = filters.CharFilter(
        label=_('Nickname'),
        lookup_expr='icontains',
    )
    rank = filters.ChoiceFilter(
        choices=TheoristRankChoices.choices,
        field_name='rank',
        label=_('Rank'),
    )

    class Meta:
        model = Theorist
        fields = (
            'full_name',
            'rank',
        )
