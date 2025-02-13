from django.db import models
from django_lifecycle import (
    LifecycleModel,
    hook,
    AFTER_UPDATE,
    AFTER_CREATE,
    AFTER_DELETE,
)

from server.common.mixins import TimeStampModelMixin, UUIDModelMixin


class Comment(UUIDModelMixin, TimeStampModelMixin, LifecycleModel):
    comment = models.TextField("comment", max_length=2000)

    post = models.ForeignKey(
        "forum.Post", related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.CustomUser",
        related_name="comments",
        on_delete=models.SET_NULL,
        null=True,
    )

    likes = models.ManyToManyField("users.CustomUser", related_name="liked_comments")
    dislikes = models.ManyToManyField(
        "users.CustomUser", related_name="disliked_comments"
    )
    likes_counter = models.PositiveSmallIntegerField(default=0)
    dislikes_counter = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "comment"
        verbose_name_plural = "comments"
        get_latest_by = "created_at"

    def __str__(self):
        return f"{self.__class__.__name__} | id - {self.id}"

    def get_absolute_url(self):
        raise NotImplementedError  # TODO: change

    @hook(AFTER_UPDATE, when_any=["likes", "dislikes"], has_changed=True)
    def after_update_likes_and_dislikes(self):
        self.likes_counter = self.likes.count()
        self.dislikes_counter = self.dislikes.count()

    @hook(AFTER_CREATE)
    @hook(AFTER_DELETE)
    def after_comments_created_or_deleted(self):
        self.post.comments_quantity = self.post.comments.count()
        self.post.save(update_fields=["comments_quantity"])
