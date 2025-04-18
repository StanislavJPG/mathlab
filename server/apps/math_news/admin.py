from django.contrib import admin

from server.apps.math_news.models import MathNews


@admin.register(MathNews)
class MathNewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'origin_url', 'improvised_published_at')
    list_filter = ('id', 'title', 'short_content', 'is_visible', 'improvised_published_at')
