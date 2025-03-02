from typing import Final

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django_lifecycle import LifecycleModel, hook, BEFORE_SAVE, AFTER_CREATE
from hitcount.models import HitCountMixin

from slugify import slugify

from server.apps.forum.managers import PostQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class Post(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel, HitCountMixin):
    CATEGORIES_LIMIT: Final[int] = 4

    title = models.CharField(max_length=85)
    content = models.TextField(max_length=2000)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    theorist = models.ForeignKey('theorist.Theorist', on_delete=models.SET_NULL, null=True, related_name='posts')
    categories = models.ManyToManyField('forum.PostCategory', related_name='posts')

    likes = models.ManyToManyField('theorist.Theorist', through='forum.PostLike', related_name='liked_posts')
    dislikes = models.ManyToManyField('theorist.Theorist', through='forum.PostDislike', related_name='disliked_posts')

    supports = models.ManyToManyField('theorist.Theorist', through='forum.PostSupport', related_name='supported_posts')

    # Denormilized fields
    likes_counter = models.PositiveSmallIntegerField(default=0)
    dislikes_counter = models.PositiveSmallIntegerField(default=0)

    hit_count_generic = GenericRelation(
        'hitcount.HitCount', object_id_field='object_pk', related_query_name='hit_count_generic_relation'
    )
    comments_quantity = models.PositiveSmallIntegerField(default=0)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        get_latest_by = 'created_at'

    def __str__(self):
        return f'{self.title} | {self.__class__.__name__} | id - {self.id}'

    def get_absolute_url(self):
        return reverse('forum:post-details', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_boringavatars_url(self):
        return reverse(
            'forum:post-avatar',
            kwargs={'uuid': self.uuid},
        )

    @hook(BEFORE_SAVE)
    def before_save(self):
        text = slugify(self.title)
        self.slug = text

    @hook(AFTER_CREATE)
    def posts_count_hook(self):
        self.theorist.total_posts = Post.objects.filter(theorist=self.theorist).count()
        self.theorist.save(update_fields=['total_posts'])

    # @hook(AFTER_UPDATE, when_any=["likes", "dislikes"], has_changed=True)
    # def after_update_likes_and_dislikes(self):
    #     self.likes_counter = self.likes.count()
    #     self.dislikes_counter = self.dislikes.count()
