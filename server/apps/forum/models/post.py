from typing import Final

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_SAVE, BEFORE_CREATE
from hitcount.models import HitCountMixin

from slugify import slugify

from server.apps.forum.managers import PostQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin
from server.common.utils.defaults import get_default_nonexistent_label


class Post(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel, HitCountMixin):
    CATEGORIES_LIMIT: Final[int] = 4

    title = models.CharField(max_length=85)
    content = models.TextField(max_length=2000)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    theorist = models.ForeignKey('theorist.Theorist', on_delete=models.SET_NULL, null=True, related_name='posts')
    theorist_full_name = models.CharField(
        max_length=255, blank=True
    )  # denormilized field because of `on_delete=models.SET_NULL` on the FK above

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

    @hook(BEFORE_CREATE)
    def before_create(self):
        if hasattr(self.theorist, 'full_name'):
            self.theorist_full_name = self.theorist.full_name
        else:
            self.theorist_full_name = get_default_nonexistent_label()

    @hook(AFTER_SAVE)
    def after_save(self):
        text = slugify(self.title)
        self.slug = text
        self.save(update_fields=['slug'], skip_hooks=True)

    @hook(AFTER_CREATE)
    def posts_count_hook(self):
        if hasattr(self.theorist, 'total_posts'):
            self.theorist.total_posts = Post.objects.filter(theorist=self.theorist).count()
            self.theorist.save(update_fields=['total_posts'])
