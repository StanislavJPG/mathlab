from datetime import timedelta, date

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.cache import cache
from django.http import Http404
from django.db.models import Q, Count

from server.apps.forum.models import Post
from server.apps.forum.serializers import PostSerializer


class PaginationCreator:
    def __init__(self, page: str, limit: int) -> None:
        self.page = page
        self.limit = limit

    @property
    def get_offset(self) -> int:
        try:
            page = int(self.page)
        except (TypeError, ValueError):
            page = 1

        if page > 0:
            return (page - 1) * self.limit
        else:
            raise Http404()

    @property
    def get_page(self) -> int:
        try:
            return int(self.page)
        except (TypeError, ValueError):
            return 1


def sort_posts(order_by, serializer, offset: int, tags: str = None):
    if order_by == "last-week":
        if not tags:
            tags = [x[0] for x in Post.CATEGORY_CHOICES]
        else:
            tags = [k for k, v in Post.CATEGORY_CHOICES if v in tags.split(",")]

        today = date.today()
        week_ago = today - timedelta(days=7)
        two_weeks_ago = week_ago - timedelta(days=7)

        # time between gte two weeks ago and lte week ago == last week
        posts = (
            Post.objects.annotate(
                comments_quantity=Count("comment"),
                likes=Count("post_likes"),
                dislikes=Count("post_dislikes"),
            )
            .prefetch_related("post_likes", "post_dislikes")
            .select_related("user")
            .filter(
                Q(created_at__gte=two_weeks_ago)
                & Q(created_at__lte=week_ago)
                & Q(categories__contains=tags)
            )
            .distinct()
            .order_by("-created_at")[offset : offset + 10]
        )

        serializer = PostSerializer(posts, many=True)
        return serializer.data

    elif order_by == "popular":
        return sorted(
            serializer.data, key=lambda x: x["comments_quantity"], reverse=True
        )

    elif order_by == "interest":
        return sorted(serializer.data, key=lambda x: x["likes"], reverse=True)

    elif order_by == "newest":
        return sorted(serializer.data, key=lambda x: x["created_at"], reverse=True)

    else:
        raise Http404()


def get_by_arguments(tags: str, offset: int, search_pattern: str) -> Post:
    posts = (
        Post.objects.select_related("user")
        .prefetch_related("post_likes", "post_dislikes")
        .annotate(
            comments_quantity=Count("comment"),
            likes=Count("post_likes", distinct=True),
            dislikes=Count("post_dislikes", distinct=True),
        )
        .distinct()
    )

    if search_pattern:
        vector = SearchVector("title")
        query = SearchQuery(search_pattern)
        posts = (
            posts.annotate(rank=SearchRank(vector, query))
            .order_by("-rank")
            .filter(rank__gt=0)
        )

    if tags:
        tags = [k for k, v in Post.CATEGORY_CHOICES if v in tags.split(",")]
        posts = posts.filter(categories__contains=tags)

    return posts[offset : offset + 10]


def sort_comments(order_by, serializer):
    if order_by == "popular" or order_by is None:
        # popular is sort by comment likes
        return sorted(serializer.data, key=lambda x: x["likes_count"], reverse=True)

    elif order_by == "created_at":
        return sorted(serializer.data, key=lambda x: x["created_at"], reverse=True)

    else:
        raise Http404()


def delete_keys_matching_pattern(*pattern):
    patterns = pattern if isinstance(pattern, tuple) else (pattern,)

    for pattern_key in patterns:
        keys_to_delete = cache.keys(pattern_key)
        cache.delete_many(keys_to_delete)
