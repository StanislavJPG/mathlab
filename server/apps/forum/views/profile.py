import os
import time

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Prefetch

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView

from server.apps.forum.models import Post
from server.apps.forum.models import Comment
from server.apps.forum.serializers import PostSerializer, CommentLastActionsSerializer
from server.common.utils.cache import delete_keys_matching_pattern
from server.apps.users.models import CustomUser as User, ProfileImage
from server.apps.users.serializers import ProfileSerializer, UserSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, user_id: int, username: str):
        try:
            cached_data = cache.get(f"profile.{user_id}.{username}")
            if not cached_data:
                user = (
                    User.objects.defer(
                        "date_joined", "is_active", "groups", "user_permissions"
                    )
                    .prefetch_related(
                        Prefetch(
                            lookup="post_set",
                            queryset=Post.objects.order_by("-created_at")[:5],
                            to_attr="recent_posts",
                        ),
                        Prefetch(
                            lookup="comment_set",
                            queryset=Comment.objects.order_by("-created_at")[:5],
                            to_attr="recent_comments",
                        ),
                    )
                    .get(pk=user_id)
                )

                user_serializer = UserSerializer(user)
                post_serializer = PostSerializer(user.recent_posts, many=True)
                comments_serializer = CommentLastActionsSerializer(
                    user.recent_comments, many=True
                )

                requested_user_image = ProfileSerializer.get_profile_image(
                    user_pk=user_id
                )
                current_user_image = ProfileSerializer.get_profile_image(
                    user_pk=request.user.id
                )

                all_actions = sorted(
                    post_serializer.data + comments_serializer.data,
                    key=lambda x: x["created_at"],
                    reverse=True,
                )
                context = {
                    "user_content": user_serializer.data,
                    "all_actions": all_actions,
                    "profile_image": requested_user_image,
                    "current_user_image": current_user_image,
                }
                cache.set(f"profile.{user_id}.{username}", context, 120)
            else:
                context = cached_data

            return render(request, "user/profile.html", context=context)
        except IndexError:
            raise Http404()

    def post(self, request, user_id: int, username: str):
        image = request.FILES["image"]
        user = get_object_or_404(get_user_model(), pk=request.user.id)

        try:
            curr_user_img = ProfileImage.objects.get(user=user)
            old_image_path = curr_user_img.image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

            curr_user_img.image = image
        except ObjectDoesNotExist:
            curr_user_img = ProfileImage(image=image, user=user)

        curr_user_img.save()
        time.sleep(3)
        delete_keys_matching_pattern(["profile*", "user_image*"])

        return HttpResponseRedirect(
            reverse("forum-profile", kwargs={"user_id": user_id, "username": username})
        )
