from typing import Final

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_lifecycle import (
    LifecycleModel,
    hook,
    AFTER_CREATE,
    AFTER_DELETE,
    BEFORE_CREATE,
)
from django_page_resolver.models import PageResolverModel

from server.apps.forum.constants import COMMENTS_LIST_PAGINATED_BY
from server.apps.forum.managers import CommentQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin
from server.common.utils.defaults import get_default_nonexistent_label


class Comment(UUIDModelMixin, TimeStampedModelMixin, PageResolverModel, LifecycleModel):
    MAX_ANSWERS_LIMIT: Final[int] = 30
    COMMENT_ANSWERS_AVAILABLE_PERIOD_DAYS_LIMIT: Final[int] = 30

    comment = models.TextField('comment', max_length=2000)

    post = models.ForeignKey('forum.Post', related_name='comments', on_delete=models.CASCADE)
    theorist = models.ForeignKey(
        'theorist.Theorist',
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True,
    )
    theorist_full_name = models.CharField(
        max_length=255, blank=True
    )  # denormilized field because of `on_delete=models.SET_NULL` on the FK above

    likes = models.ManyToManyField('theorist.Theorist', through='forum.CommentLike', related_name='liked_comments')
    dislikes = models.ManyToManyField(
        'theorist.Theorist',
        through='forum.CommentDislike',
        related_name='disliked_comments',
    )
    supports = models.ManyToManyField(
        'theorist.Theorist', through='forum.CommentSupport', related_name='supported_comments'
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

    def get_absolute_url(self, post_page: int = None):
        post_page = post_page or self.post.get_page_from_nested_object(
            target_child_instance=self, order_by='created_at', items_per_page=COMMENTS_LIST_PAGINATED_BY
        )
        return (
            reverse('forum:post-details', kwargs={'pk': self.post.pk, 'slug': self.post.slug})
            + f'?page={post_page}&comment={self.uuid}'
        )

    @hook(BEFORE_CREATE)
    def before_create(self):
        if hasattr(self.theorist, 'full_name'):
            self.theorist_full_name = self.theorist.full_name
        else:
            self.theorist_full_name = get_default_nonexistent_label()

    @hook(AFTER_CREATE)
    def comments_count_hook(self):
        self.theorist.total_comments = Comment.objects.filter(theorist=self.theorist).count()
        self.theorist.save(update_fields=['total_comments'])

    @hook(AFTER_CREATE)
    @hook(AFTER_DELETE)
    def after_comments_created_or_deleted(self):
        self.post.comments_quantity = self.post.comments.count()
        self.post.save(update_fields=['comments_quantity'])

    @property
    def check_is_answers_limitation(self):
        return self.answers.count() <= self.MAX_ANSWERS_LIMIT

    @property
    def is_able_to_get_answers(self) -> bool:
        # time_limitations = (timezone.now() - self.created_at).days <= self.COMMENT_ANSWERS_AVAILABLE_PERIOD_DAYS_LIMIT # maybe not necessary
        time_limitations = True  # const for now
        objects_limitations = self.check_is_answers_limitation
        return time_limitations and objects_limitations


class CommentAnswer(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    text_body = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(400)], max_length=400)

    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE, related_name='answers')
    theorist = models.ForeignKey(
        'theorist.Theorist', on_delete=models.SET_NULL, null=True, related_name='comment_answers'
    )
    theorist_full_name = models.CharField(
        max_length=255, blank=True
    )  # denormilized field because of `on_delete=models.SET_NULL` on the FK above

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Comment Answer')
        verbose_name_plural = _('Comment Answers')

    def __str__(self):
        return f'{self.__class__.__name__} | id - {self.id}'

    def clean(self):
        if not self.pk:
            if self.comment.answers.count() >= Comment.MAX_ANSWERS_LIMIT:
                raise ValidationError('Maximum number of answers reached.')

    @hook(BEFORE_CREATE)
    def before_create(self):
        if hasattr(self.theorist, 'full_name'):
            self.theorist_full_name = self.theorist.full_name
        else:
            self.theorist_full_name = get_default_nonexistent_label()
