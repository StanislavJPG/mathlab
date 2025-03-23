from django.contrib import admin

from server.apps.drafts.models import TheoristDrafts


@admin.register(TheoristDrafts)
class DraftsAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description')
