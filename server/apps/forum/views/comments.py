from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.http import HttpResponse

from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event
from render_block import render_block_to_string

from server.apps.forum.forms import CommentCreateForm
from server.apps.forum.models import Comment, Post
from server.common.http import AuthenticatedHttpRequest


__all__ = (
    "CommentListView",
    "CommentCreateView",
    "CommentDeleteView",
    "HXCommentQuantityView",
    "HXCommentLikesAndDislikesView",
)


class CommentListView(ListView):
    paginate_by = 10
    model = Comment
    context_object_name = "comments"
    template_name = "partials/comments_block.html"

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .filter(post__uuid=self.kwargs["post_uuid"])
            .with_likes_counters()
            .with_have_rates_per_user(self.request.user.id)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.get(uuid=self.kwargs["post_uuid"])
        return context


class CommentCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    # TODO: check LoginRequiredMixin from braces or not
    model = Comment
    template_name = "partials/comment_block_create.html"
    form_valid_message = _("Your comment has been added.")
    form_invalid_message = _("Error. Please, check your input and try again.")
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.get(uuid=self.kwargs["post_uuid"])
        return context

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "post": Post.objects.get(uuid=self.kwargs["post_uuid"]),
                "user": self.request.user,
            }
        )
        return kwargs

    def form_valid(self, form):
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponse()
        trigger_client_event(response, "commentBlockChanged")
        return response


class CommentDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    model = Comment
    template_name = "question_page.html"
    form_valid_message = _("Your comment has been deleted.")
    form_invalid_message = _("Error. Please, check your input and try again.")
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = HttpResponse()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        trigger_client_event(response, "commentBlockChanged")
        return response


class HXCommentQuantityView(DetailView):
    model = Post
    template_name = "question_page.html"
    slug_field = "uuid"
    slug_url_kwarg = "post_uuid"

    def get(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        if not self.request.htmx:
            return HttpResponse(status=405)

        self.object = self.get_object()
        context = {"comment_quantity": self.object.comments.count()}

        rendered_block = render_block_to_string(
            self.template_name,
            "comment_quantity",
            context=context,
            request=self.request,
        )
        response = HttpResponse(content=rendered_block)
        return response


class HXCommentLikesAndDislikesView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = "partials/comments_block.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return (
            super()
            .get_queryset()
            .prefetch_related("likes", "dislikes")
            .with_likes_counters()
            .with_have_rates_per_user(self.request.user.id)
        )

    def dispatch(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        if not self.request.htmx:
            return HttpResponse(status=405)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        self.object = self.get_object()

        context = {
            "comment": self.object,
        }

        rendered_block = render_block_to_string(
            self.template_name,
            "comment_likes_and_dislikes",
            context=context,
            request=self.request,
        )
        response = HttpResponse(content=rendered_block)
        return response

    def post(self, request, *args, **kwargs):
        request: AuthenticatedHttpRequest
        self.object = self.get_object()
        likes_manager = self.object.likes
        dislikes_manager = self.object.dislikes

        is_like = self.request.GET.get("like") == "true"

        if is_like:
            if likes_manager.filter(id=request.user.id).exists():
                likes_manager.remove(request.user)
            else:
                dislikes_manager.remove(request.user)
                likes_manager.add(request.user)
        else:
            if dislikes_manager.filter(id=request.user.id).exists():
                dislikes_manager.remove(request.user)
            else:
                likes_manager.remove(request.user)
                dislikes_manager.add(request.user)

        response = HttpResponse()
        trigger_client_event(
            response, f"commentLikesAndDislikesChanged{self.object.uuid}"
        )

        return response
