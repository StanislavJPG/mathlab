from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import F, Count
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import DeleteView
from rest_framework import viewsets
from rest_framework.decorators import throttle_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import Request

from server.common.templatetags.urls import url_hyphens_replace
from server.apps.users.utils import make_rate
from server.apps.users.serializers import ProfileSerializer
from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer
from ..utils import PaginationCreator, sort_comments
from server.common.utils.cache import delete_keys_matching_pattern


class QuestionCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)
        return render(
            request,
            "add_question_page.html",
            context={
                "categories": enumerate(Post.CATEGORY_CHOICES, start=1),
                "current_user_image": image_serializer,
            },
        )

    @throttle_classes([UserRateThrottle])
    def post(self, request):
        title = request.POST.get("title")
        requested_categories = [int(c) for c in request.POST.getlist("category")]
        content = request.POST.get("content")
        post = PostSerializer(
            data={"title": title, "content": content},
            context={"request": request, "requested_categories": requested_categories},
        )
        post.is_valid(raise_exception=True)
        post.save()

        delete_keys_matching_pattern("base_page*")
        url_post_title = url_hyphens_replace(post.data["title"])

        return HttpResponseRedirect(
            f"/forum/question/{post.data['id']}/{url_post_title}"
        )


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "base/forum_base.html"
    # slug_url_kwarg = 'id'
    pk_url_kwarg = "id"

    def get_queryset(self):
        return super().get_queryset().filter(user__id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return HttpResponse()


class QuestionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, q_id: int, title: str):
        order_by = request.GET.get("order_by")
        page = request.GET.get("page")
        cached_data = cache.get(f"question.{q_id}.{title}.{order_by}.{page}", None)

        if not cached_data:
            image_serializer = ProfileSerializer.get_profile_image(
                user_pk=request.user.id
            )

            post = (
                Post.objects.annotate(
                    likes=Count("post_likes", distinct=True),
                    dislikes=Count("post_dislikes", distinct=True),
                    comments_quantity=Count("comment", distinct=True),
                )
                .select_related("user")
                .prefetch_related("post_likes", "post_dislikes")
                .get(pk=q_id)
            )
            post_serializer = PostSerializer(post)

            if url_hyphens_replace(post_serializer.data["title"]) != title:
                raise Http404()

            pagination = PaginationCreator(page, limit=6)
            offset = pagination.get_offset

            if f"post_viewed_{q_id}" not in request.session:
                Post.objects.filter(pk=q_id).update(post_views=F("post_views") + 1)
                request.session[f"post_viewed_{q_id}"] = True

            comments = (
                Comment.objects.select_related("user", "post")
                .prefetch_related("likes", "dislikes")
                .annotate(likes_count=Count("likes"), dislikes_count=Count("dislikes"))
                .filter(post=post)[offset : offset + 6]
            )

            comments_serializer = CommentSerializer(comments, many=True)
            context = {
                "post": post_serializer.data,
                "pages": post.comments_quantity,
                "current_user_image": image_serializer,
                "comments": sort_comments(order_by, comments_serializer),
            }
            cache.set(f"question.{q_id}.{title}.{order_by}.{page}", context, 120)
        else:
            context = cached_data
        return render(request, "question_page.html", context=context)

    @throttle_classes([UserRateThrottle])
    def create_comment(self, request, q_id: int, title: str):
        comment = request.POST.get("comment")
        comment = CommentSerializer(
            data={"comment": comment, "post": q_id}, context={"request": request}
        )
        comment.is_valid(raise_exception=True)
        comment.save()

        delete_keys_matching_pattern(f"question.{q_id}*", f"profile.{request.user.id}*")
        return HttpResponseRedirect(f"/forum/question/{q_id}/{title}")

    @throttle_classes([UserRateThrottle])
    def create_post_rate(self, request, q_id: int, title: str):
        like = request.POST.get("like")
        dislike = request.POST.get("dislike")
        current_user: Request = request.user.id

        reactions_counters = (
            Post.objects.prefetch_related("post_likes", "post_dislikes")
            .annotate(
                likes_counter=Count("post_likes"),
                dislikes_counter=Count("post_dislikes"),
            )
            .get(pk=q_id)
        )
        post_reactions_serializer = PostSerializer(reactions_counters)

        if like and not dislike:
            if current_user not in post_reactions_serializer.data["post_likes"]:
                if current_user in post_reactions_serializer.data["post_dislikes"]:
                    reactions_counters.post_dislikes.remove(current_user)
                else:
                    make_rate(request, reactions_counters.user, score=5)
                reactions_counters.post_likes.add(current_user)
        else:
            if current_user not in post_reactions_serializer.data["post_dislikes"]:
                reactions_counters.post_likes.remove(current_user)
                reactions_counters.post_dislikes.add(current_user)

        delete_keys_matching_pattern(f"question.{q_id}*")
        return HttpResponseRedirect(f"/forum/question/{q_id}/{title}")

    @throttle_classes([UserRateThrottle])
    def create_comment_rate(self, request, q_id: int, title: str):
        like = request.POST.get("like")
        dislike = request.POST.get("dislike")
        comm_id = request.POST.get("comm_id")
        user_id = int(request.POST.get("user_id"))
        current_user: Request = request.user.id

        comment = (
            Comment.objects.prefetch_related("likes", "dislikes")
            .annotate(likes_counter=Count("likes"), dislikes_counter=Count("dislikes"))
            .get(pk=comm_id, post=q_id, user=user_id)
        )
        comment_serializer = CommentSerializer(comment)

        if like and not dislike:
            if current_user not in comment_serializer.data["likes"]:
                if current_user in comment_serializer.data["dislikes"]:
                    comment.dislikes.remove(current_user)
                else:
                    make_rate(request, comment.user, score=10)
                comment.likes.add(current_user)
        else:
            if current_user not in comment_serializer.data["dislikes"]:
                comment.likes.remove(current_user)
                comment.dislikes.add(current_user)

        delete_keys_matching_pattern(f"question.{q_id}*")
        return HttpResponseRedirect(f"/forum/question/{q_id}/{title}")

    @throttle_classes([UserRateThrottle])
    def delete_comment(self, request, q_id: int, title: str, comment_id: int):
        comment = Comment.objects.select_related("user").get(pk=comment_id)
        if comment.user.id == request.user.id:
            comment.delete()
        else:
            raise PermissionDenied()

        delete_keys_matching_pattern(
            f"question.{q_id}*", f"profile.{request.user.id}.*"
        )
        return HttpResponseRedirect(f"/forum/question/{q_id}/{title}")
