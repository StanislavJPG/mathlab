from django.contrib import admin

from server.apps.theorist.models import Theorist, TheoristProfileSettings


@admin.register(Theorist)
class TheoristAdmin(admin.ModelAdmin):
    list_display = (
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
