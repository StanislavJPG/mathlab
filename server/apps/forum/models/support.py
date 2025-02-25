from django.db import models

from server.common.mixins.models import TimeStampedModelMixin


__all__ = (
    'PostSupport',
    'CommentSupport',
)


class PostSupport(TimeStampedModelMixin):
    theorist = models.ForeignKey('theorist.Theorist', on_delete=models.CASCADE, related_name='post_supports_relation')
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('theorist', 'post'),)


class CommentSupport(TimeStampedModelMixin):
    theorist = models.ForeignKey(
        'theorist.Theorist', on_delete=models.CASCADE, related_name='comment_supports_relation'
    )
    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('theorist', 'comment'),)
