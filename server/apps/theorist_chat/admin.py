from django.contrib import admin

from server.apps.theorist_chat.models import TheoristChatRoom, TheoristMessage


@admin.register(TheoristChatRoom)
class TheoristChatRoomAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'first_member',
        'second_member',
    )


@admin.register(TheoristMessage)
class TheoristMessageAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'message',
        'sender',
    )
    list_filter = ('uuid', 'room', 'sender')
