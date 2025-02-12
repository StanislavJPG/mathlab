from django.db import models

from server.apps.forum.choices import PostTypeChoices
from server.common.mixins import TimeStampModelMixin


class PostCategory(TimeStampModelMixin):
    CATEGORY_CHOICES = PostTypeChoices
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} | {self.__class__.__name__} | id - {self.id}"

    @classmethod
    def create_data(cls):
        assert PostCategory.objects.count() == len(PostCategory.CATEGORY_CHOICES)
        for category in cls.CATEGORY_CHOICES.values:
            cls.objects.create(name=category)
