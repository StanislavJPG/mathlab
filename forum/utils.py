from datetime import timedelta

from django.core.cache import cache
from django.http import Http404
from django.utils import timezone

from forum.models import Post
from forum.serializers import PostSerializer


def make_offset(page: int, limit: int):
    if page > 0:
        return (page - 1) * limit
    else:
        raise Http404()


def sort_posts(order_by, serializer, offset):
    if order_by == 'last-week':
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        posts = Post.objects.filter(created_at__lte=start_date
                                    ).order_by('-created_at')[offset:offset + 10]
        serializer = PostSerializer(posts, many=True)
        return serializer.data

    elif order_by == 'popular':
        return sorted(serializer.data, key=lambda x: x['comments_quantity'], reverse=True)

    elif order_by == 'interest':
        return sorted(serializer.data, key=lambda x: x['likes'], reverse=True)

    elif order_by == 'newest':
        return sorted(serializer.data, key=lambda x: x['created_at'], reverse=True)

    else:
        raise Http404()


def sort_comments(order_by, serializer):
    if order_by == 'popular' or order_by is None:
        # popular is sort by comment likes
        return sorted(serializer.data, key=lambda x: x['likes'], reverse=True)

    elif order_by == 'created_at':
        return sorted(serializer.data, key=lambda x: x['created_at'], reverse=True)

    else:
        raise Http404()


def delete_keys_matching_pattern(*pattern):
    patterns = pattern if isinstance(pattern, tuple) else [pattern]

    for pattern_key in patterns:
        keys_to_delete = cache.keys(pattern_key)
        cache.delete_many(keys_to_delete)
