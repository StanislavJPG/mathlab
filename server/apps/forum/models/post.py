from django.db import models
from django.urls import reverse
from django_lifecycle import LifecycleModel, hook, AFTER_UPDATE

from server.common.mixins import TimeStampModelMixin


class Post(TimeStampModelMixin, LifecycleModel):
    title = models.CharField(max_length=85)
    content = models.TextField(max_length=2000)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, null=False)

    likes = models.ManyToManyField(
        "users.CustomUser", related_name="liked_posts", db_index=True
    )
    dislikes = models.ManyToManyField(
        "users.CustomUser", related_name="disliked_posts", db_index=True
    )

    likes_counter = models.PositiveSmallIntegerField(default=0)
    dislikes_counter = models.PositiveSmallIntegerField(default=0)
    post_views = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

    categories = models.ManyToManyField("forum.PostCategory", related_name="posts")

    class Meta:
        ordering = ("title",)
        verbose_name = "post"
        verbose_name_plural = "posts"
        get_latest_by = "created_at"

    def __str__(self):
        return f"{self.title} | {self.__class__.__name__} | id - {self.id}"

    def get_absolute_url(self):
        return reverse("forum:q", kwargs={"pk": self.pk, "slug": self.slug})

    @hook(AFTER_UPDATE, when_any=["likes", "dislikes"], has_changed=True)
    def after_update_likes_and_dislikes(self):
        self.likes_counter = self.likes.count()
        self.dislikes_counter = self.dislikes.count()
