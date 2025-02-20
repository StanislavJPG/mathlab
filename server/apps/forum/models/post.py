from django.db import models
from django.urls import reverse
from django_lifecycle import LifecycleModel, hook, BEFORE_SAVE

from slugify import slugify

from server.apps.forum.managers import PostQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class Post(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    title = models.CharField(max_length=85)
    content = models.TextField(max_length=2000)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    theorist = models.ForeignKey(
        "theorist.Theorist", on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    categories = models.ManyToManyField("forum.PostCategory", related_name="posts")

    likes = models.ManyToManyField(
        "theorist.Theorist", through="forum.PostLike", related_name="liked_posts"
    )
    dislikes = models.ManyToManyField(
        "theorist.Theorist", through="forum.PostDislike", related_name="disliked_posts"
    )

    # Denormilized fields
    likes_counter = models.PositiveSmallIntegerField(default=0)
    dislikes_counter = models.PositiveSmallIntegerField(default=0)

    post_views = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    comments_quantity = models.PositiveSmallIntegerField(default=0)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "post"
        verbose_name_plural = "posts"
        get_latest_by = "created_at"

    def __str__(self):
        return f"{self.title} | {self.__class__.__name__} | id - {self.id}"

    def get_absolute_url(self):
        return reverse("forum:post-details", kwargs={"pk": self.pk, "slug": self.slug})

    @hook(BEFORE_SAVE)
    def before_save(self):
        text = slugify(self.title)
        self.slug = text

    # @hook(AFTER_UPDATE, when_any=["likes", "dislikes"], has_changed=True)
    # def after_update_likes_and_dislikes(self):
    #     self.likes_counter = self.likes.count()
    #     self.dislikes_counter = self.dislikes.count()
