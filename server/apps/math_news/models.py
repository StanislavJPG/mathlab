from django.db import models
from django.utils import timezone


class MathNews(models.Model):
    title = models.CharField(max_length=255, unique=True)
    new_url = models.CharField(max_length=255, unique=True)
    additional_info = models.CharField(max_length=255, null=True)
    posted = models.CharField(max_length=100)
    published_at = models.DateField(default=timezone.now)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'news'
        get_latest_by = 'published_at'

    def __str__(self):
        return f'{self.title}'
