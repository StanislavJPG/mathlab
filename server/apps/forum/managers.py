from django.db import models
from django.db.models import Count, Exists, OuterRef


class CommentQuerySet(models.QuerySet):
    def with_likes_counters(self):
        return self.annotate(
            custom_likes_counter=Count("likes", distinct=True),
            custom_dislikes_counter=Count("dislikes", distinct=True),
        )

    def with_have_rates_per_theorist(self, theorist_uuid):
        return self.annotate(
            is_comment_already_liked=Exists(
                self.model.likes.through.objects.filter(
                    comment__uuid=OuterRef("uuid"), theorist__uuid=theorist_uuid
                )
            ),
            is_comment_already_disliked=Exists(
                self.model.dislikes.through.objects.filter(
                    comment__uuid=OuterRef("uuid"), theorist__uuid=theorist_uuid
                )
            ),
        )


class PostQuerySet(models.QuerySet):
    def with_likes_counters(self):
        return self.annotate(
            custom_likes_counter=Count("likes", distinct=True),
            custom_dislikes_counter=Count("dislikes", distinct=True),
        )

    def with_have_rates_per_theorist(self, theorist_uuid):
        return self.annotate(
            is_already_liked=Exists(
                self.model.likes.through.objects.filter(
                    post__uuid=OuterRef("uuid"), theorist__uuid=theorist_uuid
                )
            ),
            is_already_disliked=Exists(
                self.model.dislikes.through.objects.filter(
                    post__uuid=OuterRef("uuid"), theorist__uuid=theorist_uuid
                )
            ),
        )
