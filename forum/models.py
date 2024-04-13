from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from users.models import CustomUser as User


class Category(models.Model):
    category_name = models.CharField('category_name', max_length=100)

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    title = models.CharField('title', max_length=85)
    content = models.TextField('content', max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    categories = models.ManyToManyField(Category)
    likes = models.IntegerField('likes', default=0)

    class Meta:
        ordering = ('title',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        get_latest_by = 'created_at'

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    comment = models.TextField('comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.comment}'
