from braces.views import FormMessagesMixin

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, CreateView, DetailView

from server.apps.forum.models import Post, Comment


class QuestionView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "question_page.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.get_object())
        context.update({"comments": comments})
        return context


# class QuestionView(viewsets.ViewSet):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get(self, request, q_id: int, title: str):
#         order_by = request.GET.get("order_by")
#         page = request.GET.get("page")
#
#         image_serializer = ProfileSerializer.get_profile_image(
#             user_pk=request.user.id
#         )
#
#         post = (
#             Post.objects.annotate(
#                 likes=Count("post_likes", distinct=True),
#                 dislikes=Count("post_dislikes", distinct=True),
#                 comments_quantity=Count("comment", distinct=True),
#             )
#             .select_related("user")
#             .prefetch_related("post_likes", "post_dislikes")
#             .get(pk=q_id)
#         )
#         post_serializer = PostSerializer(post)
#
#         pagination = PaginationCreator(page, limit=6)
#         offset = pagination.get_offset
#
#         if f"post_viewed_{q_id}" not in request.session:
#             Post.objects.filter(pk=q_id).update(post_views=F("post_views") + 1)
#             request.session[f"post_viewed_{q_id}"] = True
#
#         comments = (
#             Comment.objects.select_related("user", "post")
#             .prefetch_related("likes", "dislikes")
#             .annotate(likes_count=Count("likes"), dislikes_count=Count("dislikes"))
#             .filter(post=post)[offset : offset + 6]
#         )
#
#         comments_serializer = CommentSerializer(comments, many=True)
#         context = {
#             "post": post_serializer.data,
#             "pages": post.comments_quantity,
#             "current_user_image": image_serializer,
#             "comments": sort_comments(order_by, comments_serializer),
#         }
#         cache.set(f"question.{q_id}.{title}.{order_by}.{page}", context, 120)
#         return render(request, "question_page.html", context=context)
#
#     @throttle_classes([UserRateThrottle])
#     def create_comment(self, request, q_id: int, title: str):
#         comment = request.POST.get("comment")
#         comment = CommentSerializer(
#             data={"comment": comment, "post": q_id}, context={"request": request}
#         )
#         comment.is_valid(raise_exception=True)
#         comment.save()
#
#         delete_keys_matching_pattern(f"question.{q_id}*", f"profile.{request.user.id}*")
#         return HttpResponseRedirect(f"/forum/question/{q_id}/{title}")
#
#     @throttle_classes([UserRateThrottle])
#     def create_post_rate(self, request, q_id: int, title: str):
#         like = request.POST.get("like")
#         dislike = request.POST.get("dislike")
#         current_user: Request = request.user.id
#
#         reactions_counters = (
#             Post.objects.prefetch_related("post_likes", "post_dislikes")
#             .annotate(
#                 likes_counter=Count("post_likes"),
#                 dislikes_counter=Count("post_dislikes"),
#             )
#             .get(pk=q_id)
#         )
#         post_reactions_serializer = PostSerializer(reactions_counters)
#
#         if like and not dislike:
#             if current_user not in post_reactions_serializer.data["post_likes"]:
#                 if current_user in post_reactions_serializer.data["post_dislikes"]:
#                     reactions_counters.post_dislikes.remove(current_user)
#                 else:
#                     make_rate(request, reactions_counters.user, score=5)
#                 reactions_counters.post_likes.add(current_user)
#         else:
#             if current_user not in post_reactions_serializer.data["post_dislikes"]:
#                 reactions_counters.post_likes.remove(current_user)
#                 reactions_counters.post_dislikes.add(current_user)
#
#         delete_keys_matching_pattern(f"question.{q_id}*")
#         return HttpResponseRedirect(f"/forum/question/{q_id}/{title}")
#
#     @throttle_classes([UserRateThrottle])
#     def create_comment_rate(self, request, q_id: int, title: str):
#         like = request.POST.get("like")
#         dislike = request.POST.get("dislike")
#         comm_id = request.POST.get("comm_id")
#         user_id = int(request.POST.get("user_id"))
#         current_user: Request = request.user.id
#
#         comment = (
#             Comment.objects.prefetch_related("likes", "dislikes")
#             .annotate(likes_counter=Count("likes"), dislikes_counter=Count("dislikes"))
#             .get(pk=comm_id, post=q_id, user=user_id)
#         )
#         comment_serializer = CommentSerializer(comment)
#
#         if like and not dislike:
#             if current_user not in comment_serializer.data["likes"]:
#                 if current_user in comment_serializer.data["dislikes"]:
#                     comment.dislikes.remove(current_user)
#                 else:
#                     make_rate(request, comment.user, score=10)
#                 comment.likes.add(current_user)
#         else:
#             if current_user not in comment_serializer.data["dislikes"]:
#                 comment.likes.remove(current_user)
#                 comment.dislikes.add(current_user)
#
#         delete_keys_matching_pattern(f"question.{q_id}*")
#         return HttpResponseRedirect(f"/forum/question/{q_id}/{title}")
#
#     @throttle_classes([UserRateThrottle])
#     def delete_comment(self, request, q_id: int, title: str, comment_id: int):
#         comment = Comment.objects.select_related("user").get(pk=comment_id)
#         if comment.user.id == request.user.id:
#             comment.delete()
#         else:
#             raise PermissionDenied()
#
#         delete_keys_matching_pattern(
#             f"question.{q_id}*", f"profile.{request.user.id}.*"
#         )
#         return HttpResponseRedirect(f"/forum/question/{q_id}/{title}")


class QuestionCreateForm(forms.ModelForm):  # TODO: Fix M2M SAVING
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "categories",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": _("Question topic (maximum 85 characters)")}
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": _("Describe your question here"),
                }
            ),
        }  # trans: Тема питання (не більше 85 символів)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        # prepare 'categories' field
        self.fields["categories"].label_from_instance = (
            lambda obj: obj.get_name_display()
        )
        self.instance.user = self.user


class QuestionCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    model = Post
    template_name = "add_question_page.html"
    form_class = QuestionCreateForm
    form_valid_message = _("You successfully created a new post.")
    form_invalid_message = _(
        "Error while creating post. Please check for errors and try again."
    )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        post = form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponseRedirect(post.get_absolute_url())
        return response


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "base/forum_base.html"
    pk_url_kwarg = "id"

    def get_queryset(self):
        return super().get_queryset().filter(user__id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return HttpResponse()
