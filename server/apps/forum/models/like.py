from django.db import models
from django_lifecycle import LifecycleModel

from server.common.mixins import UUIDModelMixin, TimeStampedModelMixin


class PostLike(UUIDModelMixin, LifecycleModel, TimeStampedModelMixin):
    post = models.ForeignKey("forum.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (("user", "post"),)

    # @hook(AFTER_CREATE)
    # @hook(AFTER_DELETE)
    # @hook(AFTER_UPDATE)
    # def after_update_likes(self):
    #     self.post.likes_counter = self.post.likes.count()
    #     self.post.save(update_fields=['likes_counter'])


class PostDislike(UUIDModelMixin, LifecycleModel, TimeStampedModelMixin):
    post = models.ForeignKey("forum.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (("user", "post"),)


class CommentLike(UUIDModelMixin, LifecycleModel, TimeStampedModelMixin):
    comment = models.ForeignKey("forum.Comment", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (("user", "comment"),)


class CommentDislike(UUIDModelMixin, LifecycleModel, TimeStampedModelMixin):
    comment = models.ForeignKey("forum.Comment", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (("user", "comment"),)
