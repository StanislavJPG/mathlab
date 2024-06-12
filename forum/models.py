from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser as User


class Category(models.Model):
    category_name = models.CharField('category_name', max_length=100)

    def __str__(self):
        return f'{self.category_name}'

    CATEGORIES: tuple = ('Графіки функцій', 'Матриці', 'Рівняння', 'Нерівності',
                         'Системи', 'Вища математика', 'Теорії ймовірностей',
                         'Комбінаторика', 'Дискретна математика', 'Початкова математика', 'Відсотки',
                         'Тригонометрія', 'Геометрія', 'Ймовірність і статистика', 'Алгоритми', 'Інше', 'Алгебра')


class Post(models.Model):
    title = models.CharField(_('title'), max_length=85)
    content = models.TextField(_('content'), max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    categories = models.ManyToManyField(Category, related_name='post_categories', db_index=True)
    modified_at = models.DateTimeField(default=timezone.now)
    post_likes = models.ManyToManyField(get_user_model(), related_name='liked_posts', db_index=True)
    post_dislikes = models.ManyToManyField(get_user_model(), related_name='disliked_posts', db_index=True)
    post_views = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        get_latest_by = 'created_at'
        indexes = [
            models.Index(fields=('created_at',)),
            models.Index(fields=('modified_at',)),
            models.Index(fields=('post_views',))
        ]

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    comment = models.TextField('comment', max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_comments', default=0)
    dislikes = models.ManyToManyField(get_user_model(), related_name='disliked_comments', default=0)
    modified_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f'{self.comment}'
