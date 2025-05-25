from typing import Final

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_lifecycle import hook, AFTER_CREATE, LifecycleModel

from server.apps.math_news.querysets import MathNewsQueryset
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin
from server.common.utils.helpers import generate_randon_hex_colors


def default_background_colors():
    return ['#eeaeca', '#94bbe9']


class MathNews(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    NUM_OF_BACKGROUND_COLORS: Final[int] = 2

    title = models.CharField(max_length=255)
    short_content = models.TextField(max_length=255, null=True)

    origin_url = models.URLField(null=True, unique=True)

    improvised_published_at = models.CharField(
        null=True, editable=False
    )  # actually, this is deprecated and will be removed or replaced in the future

    is_visible = models.BooleanField(default=True)

    background_colors = ArrayField(
        models.CharField(max_length=200), blank=True, size=NUM_OF_BACKGROUND_COLORS, default=default_background_colors
    )

    objects = MathNewsQueryset.as_manager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'news'
        get_latest_by = 'created_at'

    def __str__(self):
        return f'{self.title} | {self.__class__.__name__} | id - {self.id}'

    @hook(AFTER_CREATE)
    def after_create(self):
        colors = generate_randon_hex_colors(number_of_colors=self.NUM_OF_BACKGROUND_COLORS)
        self.background_colors = colors
        self.save(update_fields=['background_colors'])

    @classmethod
    def save_unique_news(cls, titles):
        to_create = []
        for title in titles:
            if not cls.objects.filter(origin_url=title['origin_url']).exists():
                to_create.append(cls(**title))
        objs = cls.objects.bulk_create(to_create)

        for obj in objs:
            obj.after_create()  # because bulk_create use only one create() method

        return objs
