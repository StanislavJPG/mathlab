from django.views.generic import ListView

from server.apps.forum.models import Post, PostCategory


class ForumBaseView(ListView):
    paginate_by = 10
    model = Post
    context_object_name = "posts"
    template_name = "posts_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = PostCategory.objects.all()
        return context
