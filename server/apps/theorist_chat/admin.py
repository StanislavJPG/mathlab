from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from server.apps.theorist_chat.models import TheoristChatRoom, TheoristMessage, TheoristChatGroupConfiguration


@admin.register(TheoristChatGroupConfiguration)
class TheoristChatGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'theorist', 'is_chats_available')
    list_filter = ('theorist__full_name', 'is_chats_available')


@admin.register(TheoristChatRoom)
class TheoristChatRoomAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'first_member',
        'second_member',
    )
    search_fields = ('first_member__full_name', 'second_member__full_name')


class VoiceMessageFilter(admin.SimpleListFilter):
    title = _('voice message')
    parameter_name = 'is_voice_message'

    def lookups(self, request, model_admin):
        return [
            ('0', _('No')),
            ('1', _('Yes')),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(audio_message__isnull=True)
        if self.value() == '1':
            return queryset.filter(message='', audio_message__isnull=False)


@admin.register(TheoristMessage)
class TheoristMessageAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'message',
        'sender',
    )
    list_filter = (
        'created_at',
        'is_read',
        VoiceMessageFilter,
    )
