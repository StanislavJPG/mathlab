from django.contrib import admin

from server.apps.theorist.models import Theorist


@admin.register(Theorist)
class TheoristAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "score",
        "rank",
        "total_posts",
        "total_comments",
    )
    list_filter = ("full_name", "user", "rank")
    search_fields = (
        "uuid",
        "id",
        "full_name",
    )
