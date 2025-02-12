from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count
from django.views.generic import ListView

from server.apps.forum.models import Post


class ForumBaseView(ListView):
    paginate_by = 10
    model = Post
    context_object_name = "posts"
    template_name = "base/forum_base.html"

    def get_queryset(self):
        tags = self.request.GET.get("tags")
        search_pattern = self.request.GET.get("search_pattern")
        posts = (
            super()
            .get_queryset()
            .filter()
            .select_related("user")
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

        return posts
