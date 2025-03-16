from django.contrib import admin

from server.apps.carousel.models import Carousel


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_filter = ('id', 'uuid', 'title', 'is_active')
