from django.contrib import admin

from server.apps.theorist.models import (
    Theorist,
    TheoristProfileSettings,
    TheoristFriendshipBlackList,
    TheoristFriendship,
    TheoristBlacklist,
)


@admin.register(Theorist)
class TheoristAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'full_name',
        'user',
        'score',
        'rank',
        'total_posts',
        'total_comments',
    )
    list_filter = ('full_name', 'user', 'rank')
    search_fields = (
        'uuid',
        'id',
        'full_name',
    )


@admin.register(TheoristProfileSettings)
class TheoristProfileSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'theorist__user__username',
        'theorist__full_name',
    )
    list_filter = (
        'theorist__full_name',
        'theorist__user__username',
    )
    search_fields = (
        'uuid',
        'id',
        'theorist__full_name',
    )


@admin.register(TheoristFriendship)
class TheoristFriendshipAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'requester', 'receiver', 'status')
    list_filter = (
        'status',
        'created_at',
    )


class TheoristBlacklistInline(admin.TabularInline):
    model = TheoristBlacklist


@admin.register(TheoristFriendshipBlackList)
class TheoristFriendshipBlackListAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'owner')
    list_filter = ('owner',)
    inlines = (TheoristBlacklistInline,)
