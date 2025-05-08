from typing import Final

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_lifecycle import hook, AFTER_CREATE, LifecycleModel

from server.apps.carousel.querysets import CarouselQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin
from server.common.utils.helpers import generate_randon_hex_colors


def default_background_colors():
    return ['#ff7e5f', '#feb47b']


class Carousel(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    NUM_OF_BACKGROUND_COLORS: Final[int] = 2

    title = models.CharField(max_length=255)
    content = models.TextField()
    button_text = models.CharField(max_length=100, blank=True)
    button_url = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    background_colors = ArrayField(
        models.CharField(max_length=200), blank=True, size=NUM_OF_BACKGROUND_COLORS, default=default_background_colors
    )

    objects = CarouselQuerySet.as_manager()

    def __str__(self):
        return f'{self.title} | {self.__class__.__name__} | id - {self.id}'

    @hook(AFTER_CREATE)
    def after_create(self):
        colors = generate_randon_hex_colors(number_of_colors=self.NUM_OF_BACKGROUND_COLORS)
        self.background_colors = colors
        self.save(update_fields=['background_colors'])
