from django.db import models
from django_lifecycle import (
    LifecycleModel,
    hook,
    AFTER_CREATE,
    AFTER_DELETE,
)

from server.apps.forum.managers import CommentQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class Comment(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    comment = models.TextField('comment', max_length=2000)

    post = models.ForeignKey(
        'forum.Post', related_name='comments', on_delete=models.CASCADE
    )
    theorist = models.ForeignKey(
        'theorist.Theorist',
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True,
    )
    likes = models.ManyToManyField(
        'theorist.Theorist', through='forum.CommentLike', related_name='liked_comments'
    )
    dislikes = models.ManyToManyField(
        'theorist.Theorist',
        through='forum.CommentDislike',
        related_name='disliked_comments',
    )

    likes_counter = models.PositiveSmallIntegerField(default=0)
    dislikes_counter = models.PositiveSmallIntegerField(default=0)

    objects = CommentQuerySet.as_manager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        get_latest_by = 'created_at'

    def __str__(self):
        return f'{self.__class__.__name__} | id - {self.id}'

    def get_absolute_url(self):
        raise NotImplementedError  # TODO: change

    @hook(AFTER_CREATE)
    @hook(AFTER_DELETE)
    def after_comments_created_or_deleted(self):
        self.post.comments_quantity = self.post.comments.count()
        self.post.save(update_fields=['comments_quantity'])
