import django_filters as filters

from server.apps.theorist.models import Theorist


class TheoristCommunityFilter(filters.FilterSet):
    full_name = filters.CharFilter(
        lookup_expr='icontains',
    )

    class Meta:
        model = Theorist
        fields = ('full_name',)
