from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres import fields

from server.apps.users.models import CustomUser as User


class Post(models.Model):
    CATEGORY_CHOICES: tuple = (
        ("GF", "Графіки функцій"),
        ("MT", "Матриці"),
        ("RV", "Рівняння"),
        ("NR", "Нерівності"),
        ("SM", "Системи"),
        ("VM", "Вища математика"),
        ("TY", "Теорії ймовірностей"),
        ("KM", "Комбінаторика"),
        ("DM", "Дискретна математика"),
        ("PM", "Початкова математика"),
        ("VD", "Відсотки"),
        ("TG", "Тригонометрія"),
        ("GM", "Геометрія"),
        ("YS", "Ймовірність і статистика"),
        ("AL", "Алгоритми"),
        ("AG", "Алгебра"),
        ("IN", "Інше"),
    )

    title = models.CharField(_("title"), max_length=85)
    content = models.TextField(_("content"), max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    modified_at = models.DateTimeField(default=timezone.now)
    post_likes = models.ManyToManyField(
        get_user_model(), related_name="liked_posts", db_index=True
    )  # TODO: Denormilize it
    post_dislikes = models.ManyToManyField(
        get_user_model(), related_name="disliked_posts", db_index=True
    )
    post_views = models.IntegerField(default=0, null=True, blank=True)
    categories = fields.ArrayField(
        models.CharField(
            max_length=20, blank=False, choices=list(CATEGORY_CHOICES), default="IN"
        ),
        size=4,
        default=("IN",),
    )

    def get_foo_categories(self):
        lookup = {k: v for k, v in self.CATEGORY_CHOICES}
        return [lookup.get(v) for v in self.categories]

    @staticmethod
    def represent_nums_to_categories(nums: list[int]):
        return [v[0] for k, v in enumerate(Post.CATEGORY_CHOICES, start=1) if k in nums]

    class Meta:
        ordering = ("title",)
        verbose_name = "post"
        verbose_name_plural = "posts"
        get_latest_by = "created_at"
        indexes = [
            models.Index(fields=("created_at",)),
            models.Index(fields=("modified_at",)),
            models.Index(fields=("post_views",)),
        ]

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    comment = models.TextField("comment", max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(
        get_user_model(), related_name="liked_comments", default=0
    )
    dislikes = models.ManyToManyField(
        get_user_model(), related_name="disliked_comments", default=0
    )
    modified_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f"{self.comment}"
