from braces.views import LoginRequiredMixin, FormMessagesMixin
from django import forms
from django.http import HttpResponse

from django.views.generic import CreateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event
from render_block import render_block_to_string

from server.apps.forum.models import Comment, Post
from server.common.http import AuthenticatedHttpRequest


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.post = kwargs.pop("post")
        super().__init__(*args, **kwargs)
        self.instance.user = self.user
        self.instance.post = self.post


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
        trigger_client_event(response, "commentBlockChanged")
        return response


class CommentQuantityView(DetailView):
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
