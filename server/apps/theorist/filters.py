import django_filters as filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.models import TheoristFriendship


class AbstractTheoristFriendshipFilter(filters.FilterSet):
    full_name = filters.CharFilter(method='filter_by_full_name')

    class Meta:
        model = TheoristFriendship
        fields = ['full_name']

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        super().__init__(*args, **kwargs)
        self.filters['full_name'].field.widget.attrs['placeholder'] = _('Search theorist')


class TheoristPrivateFriendshipFilter(AbstractTheoristFriendshipFilter):
    def filter_by_full_name(self, queryset, name, value):
        if self.request.GET.get('is_accepted', None):
            qs_filter = Q(receiver__full_name__icontains=value) | Q(requester__full_name__icontains=value)
        else:
            qs_filter = Q(requester__full_name__icontains=value)

        return queryset.filter((~Q(receiver=self.theorist) | ~Q(requester=self.theorist)) & qs_filter)


class TheoristPublicFriendshipFilter(AbstractTheoristFriendshipFilter):
    def filter_by_full_name(self, queryset, name, value):
        if self.request.GET.get('is_accepted', None):
            qs_filter = Q(receiver__full_name__icontains=value) | Q(requester__full_name__icontains=value)
        else:
            qs_filter = Q(receiver__full_name__icontains=value)

        return queryset.filter((~Q(receiver=self.theorist) | ~Q(requester=self.theorist)) & qs_filter)
