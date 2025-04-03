import django_filters as filters
from django.db.models import Q

from django.utils.translation import gettext_lazy as _

from server.apps.theorist_chat.models import TheoristChatRoom


class MailBoxFilter(filters.FilterSet):
    username = filters.CharFilter(method='filter_by_username')

    class Meta:
        model = TheoristChatRoom
        fields = ['username']

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        super().__init__(*args, **kwargs)
        self.filters['username'].field.widget.attrs['placeholder'] = _('Find chat by name')

    def filter_by_username(self, queryset, name, value):
        return queryset.filter(
            (~Q(first_member=self.theorist) | ~Q(second_member=self.theorist))
            & (Q(first_member__full_name__icontains=value) | Q(second_member__full_name__icontains=value))
        )
