from django.contrib import admin

from server.apps.drafts.models import TheoristDrafts, TheoristDraftsConfiguration


@admin.register(TheoristDrafts)
class DraftsAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description')


@admin.register(TheoristDraftsConfiguration)
class TheoristDraftsConfigurationAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'theorist', 'is_public_available')
    list_filter = ('id', 'uuid', 'theorist', 'is_public_available')
