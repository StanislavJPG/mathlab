from django.db import models
from django.utils import timezone


class MathNews(models.Model):
    title = models.CharField(max_length=255, unique=True)
    new_url = models.CharField(max_length=255, unique=True)
    posted = models.CharField(max_length=100)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'news'
        get_latest_by = 'posted_at'

    def __str__(self):
        return f'{self.title}'
