from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.decorators import throttle_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    AllowAny,
)
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle

from server.apps.forum.models import Post
from server.apps.forum.serializers import PostSerializer
from server.apps.forum.utils import (
    PaginationCreator,
    get_by_arguments,
    sort_posts,
    delete_keys_matching_pattern,
)
from server.apps.users.serializers import ProfileSerializer


class ForumBaseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        order_by = request.GET.get("sort")
        tags = request.GET.get("tags")
        page = request.GET.get("page")
        search_pattern = request.GET.get("search_pattern")

        if order_by:
            cached_data = cache.get(
                f"base_page.{page}.{order_by}.{tags}.{search_pattern}", None
            )
            pagination = PaginationCreator(page, limit=10)
            offset = pagination.get_offset

            current_user_image_serializer = ProfileSerializer.get_profile_image(
                user_pk=request.user.id
            )
            if not cached_data:
                address_args = (
                    request.build_absolute_uri().split("/")[-1].split("page=")[0]
                    + "page="
                )
                context = {
                    "page": pagination.get_page,
                    "url": address_args,
                    "current_user_image": current_user_image_serializer,
                    "categories": Post.CATEGORY_CHOICES,
                    "order_by": order_by,
                    "search_pattern": search_pattern,
                    "tags": tags,
                }
                # using this for get by tags even if tags is None (returning default query in this case)
                posts = get_by_arguments(tags, offset, search_pattern)

                post_serializer = PostSerializer(posts[offset : offset + 10], many=True)
                context["posts"] = sort_posts(order_by, post_serializer, offset, tags)

                cache.set(
                    f"base_page.{page}.{order_by}.{tags}.{search_pattern}", context, 120
                )
            else:
                context = cached_data

            return render(request, "base/forum_base.html", context=context)
        return HttpResponseRedirect("/forum/?sort=popular&page=1")

    @throttle_classes([UserRateThrottle])
    def post(self, request):
        # delete post method
        post_id = int(request.POST.get("post_id"))
        post = Post.objects.select_related("user").get(pk=post_id)

        if post.user.id == request.user.id:
            # only post owner can delete his post
            post.delete()
            cache.clear()
        else:
            raise PermissionDenied()

        delete_keys_matching_pattern("base_page*")
        return HttpResponseRedirect("/forum/?sort=popular&page=1")

    # def get_search(self, request):
    #     search_pattern = request.GET.get('search_pattern')
    #     page = request.GET.get('page')
    #
    #     pagination = PaginationCreator(page, limit=10)
    #     offset = pagination.get_offset
    #
    #     address_args = request.build_absolute_uri().split('/')[-1].split('page=')[0] + 'page='
    #     image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)
    #     cached_data = cache.get(f'base_page.search.{search_pattern}.{page}')
    #
    #     # if not cached_data:
    #         # post = PostDocument().search().query("match", title=search_pattern)[offset:offset+10]
    #         # post_queryset = post.to_queryset()
    #         # post_serializer = PostSerializer(post_queryset, many=True)
    #         #
    #         # posts = sort_posts('newest', post_serializer, offset)
    #         # cache.set(f'base_page.search.{search_pattern}.{page}', posts, 120)
    #     # else:
    #     #     posts = cached_data
    #
    #     return render(request, 'base/forum_base.html',
    #                   context={
    #                            'page': pagination.get_page,
    #                            'url': address_args,
    #                            'current_user_image': image_serializer})


# class PostSearchView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request):
#         search_pattern = request.GET.get('search_pattern')
#         page = request.GET.get('page')
#
#         pagination = PaginationCreator(page, limit=10)
#         offset = pagination.get_offset
#
#         address_args = request.build_absolute_uri().split('/')[-1].split('page=')[0] + 'page='
#         image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)
#         cached_data = cache.get(f'base_page.search.{search_pattern}.{page}')
#
#         if not cached_data:
#             post = PostDocument().search().query("match", title=search_pattern)[offset:offset+10]
#             post_queryset = post.to_queryset()
#             post_serializer = PostSerializer(post_queryset, many=True)
#
#             posts = sort_posts('newest', post_serializer, offset)
#             cache.set(f'base_page.search.{search_pattern}.{page}', posts, 120)
#         else:
#             posts = cached_data
#
#         return render(request, 'base/forum_base.html',
#                       context={'posts': posts,
#                                'page': pagination.get_page,
#                                'url': address_args,
#                                'current_user_image': image_serializer})
