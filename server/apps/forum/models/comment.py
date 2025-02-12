from django.contrib.auth import get_user_model
from django.db import models
from django_lifecycle import LifecycleModel, hook, AFTER_UPDATE

from server.common.mixins import TimeStampModelMixin


class Comment(TimeStampModelMixin, LifecycleModel):
    comment = models.TextField("comment", max_length=2000)

    post = models.ForeignKey("forum.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)

    likes = models.ManyToManyField(get_user_model(), related_name="liked_comments")
    dislikes = models.ManyToManyField(
        get_user_model(), related_name="disliked_comments"
    )
    likes_counter = models.PositiveSmallIntegerField(default=0)
    dislikes_counter = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("id",)
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
