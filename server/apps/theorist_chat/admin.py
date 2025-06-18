from django.contrib import admin

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
    )
