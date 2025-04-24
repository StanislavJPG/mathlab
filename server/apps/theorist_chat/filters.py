import django_filters as filters
from django.db.models import Q, F

from django.utils.translation import gettext_lazy as _

from server.apps.theorist_chat.models import TheoristChatRoom


class MailBoxFilter(filters.FilterSet):
    username = filters.CharFilter(method='filter_by_username')
    show_blocked_chats = filters.BooleanFilter(method='filter_by_show_blocked_chats')

    class Meta:
        model = TheoristChatRoom
        fields = (
            'username',
            'show_blocked_chats',
        )

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        super().__init__(*args, **kwargs)
        self.filters['username'].field.widget.attrs['placeholder'] = _('Find chat by name')

    def filter_by_username(self, queryset, name, value):
        return queryset.filter(
            (~Q(first_member=self.theorist) | ~Q(second_member=self.theorist))
            & (Q(first_member__full_name__icontains=value) | Q(second_member__full_name__icontains=value))
        )

    def filter_by_show_blocked_chats(self, queryset, name, value):
        if value is False:
            return queryset.exclude(
                Q(first_member__blacklist__blocked_theorists=F('second_member'))
                | Q(second_member__blacklist__blocked_theorists=F('first_member'))
            )
        return queryset
