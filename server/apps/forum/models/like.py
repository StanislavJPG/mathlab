from django.db import models
from django_lifecycle import LifecycleModel

from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class PostLike(UUIDModelMixin, LifecycleModel, TimeStampedModelMixin):
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE)
    theorist = models.ForeignKey(
        'theorist.Theorist',
        null=True,
        on_delete=models.SET_NULL,
        related_name='post_likes_relations',
    )

    class Meta:
        unique_together = (('theorist', 'post'),)


class PostDislike(UUIDModelMixin, LifecycleModel, TimeStampedModelMixin):
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE)
    theorist = models.ForeignKey(
        'theorist.Theorist',
        null=True,
        on_delete=models.SET_NULL,
        related_name='post_dislikes_relations',
    )

    class Meta:
        unique_together = (('theorist', 'post'),)


class CommentLike(UUIDModelMixin, LifecycleModel, TimeStampedModelMixin):
    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE)
    theorist = models.ForeignKey(
        'theorist.Theorist',
        null=True,
        on_delete=models.SET_NULL,
        related_name='comment_likes_relations',
    )

    class Meta:
        unique_together = (('theorist', 'comment'),)


class CommentDislike(UUIDModelMixin, LifecycleModel, TimeStampedModelMixin):
    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE)
    theorist = models.ForeignKey(
        'theorist.Theorist',
        null=True,
        on_delete=models.SET_NULL,
        related_name='comment_dislikes_relations',
    )

    class Meta:
        unique_together = (('theorist', 'comment'),)
