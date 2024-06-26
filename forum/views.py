from django.core.cache import cache
from django.db.models import F, Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import throttle_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import Request

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .templatetags.filters import url_hyphens_replace
from .utils import PaginationCreator, sort_comments, delete_keys_matching_pattern, sort_posts, get_by_arguments
from users.utils import make_rate
from users.serializers import ProfileSerializer


class ForumBaseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        order_by = request.GET.get('sort')
        tags = request.GET.get('tags')
        page = request.GET.get('page')
        search_pattern = request.GET.get('search_pattern')

        if order_by:
            cached_data = cache.get(f'base_page.{page}.{order_by}.{tags}.{search_pattern}', None)
            pagination = PaginationCreator(page, limit=10)
            offset = pagination.get_offset

            current_user_image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)
            if not cached_data:
                address_args = request.build_absolute_uri().split('/')[-1].split('page=')[0] + 'page='
                context = {
                    'page': pagination.get_page,
                    'url': address_args,
                    'current_user_image': current_user_image_serializer,
                    'categories': Post.CATEGORY_CHOICES,
                    'order_by': order_by,
                    'search_pattern': search_pattern,
                    'tags': tags
                }
                # using this for get by tags even if tags is None (returning default query in this case)
                posts = get_by_arguments(tags, offset, search_pattern)

                post_serializer = PostSerializer(posts[offset:offset + 10], many=True)
                context['posts'] = sort_posts(order_by, post_serializer, offset, tags)

                cache.set(f'base_page.{page}.{order_by}.{tags}.{search_pattern}', context, 120)
            else:
                context = cached_data

            return render(request, 'forum/forum_base_page.html',
                          context=context)
        return HttpResponseRedirect('/forum/?sort=popular&page=1')

    @throttle_classes([UserRateThrottle])
    def post(self, request):
        # delete post method
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.select_related('user').get(pk=post_id)

        if post.user.id == request.user.id:
            # only post owner can delete his post
            post.delete()
            cache.clear()
        else:
            raise PermissionDenied()

        delete_keys_matching_pattern('base_page*')
        return HttpResponseRedirect('/forum/?sort=popular&page=1')

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
    #     return render(request, 'forum/forum_base_page.html',
    #                   context={
    #                            'page': pagination.get_page,
    #                            'url': address_args,
    #                            'current_user_image': image_serializer})


class QuestionCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)
        return render(request, 'forum/forum_add_question_page.html',
                      context={
                          'categories': enumerate(Post.CATEGORY_CHOICES, start=1),
                          'current_user_image': image_serializer
                      })

    @throttle_classes([UserRateThrottle])
    def post(self, request):
        title = request.POST.get('title')
        requested_categories = [int(c) for c in request.POST.getlist('category')]
        content = request.POST.get('content')
        post = PostSerializer(
            data={'title': title, 'content': content},
            context={'request': request, 'requested_categories': requested_categories}
        )
        post.is_valid(raise_exception=True)
        post.save()

        delete_keys_matching_pattern('base_page*')
        url_post_title = url_hyphens_replace(post.data['title'])

        return HttpResponseRedirect(f'/forum/question/{post.data["id"]}/{url_post_title}')


class QuestionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, q_id: int, title: str):
        order_by = request.GET.get('order_by')
        page = request.GET.get('page')
        cached_data = cache.get(f'question.{q_id}.{title}.{order_by}.{page}', None)

        if not cached_data:
            image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)

            post = Post.objects.annotate(
                likes=Count('post_likes', distinct=True),
                dislikes=Count('post_dislikes', distinct=True),
                comments_quantity=Count('comment', distinct=True)
            ).select_related('user').prefetch_related('post_likes', 'post_dislikes').get(pk=q_id)
            post_serializer = PostSerializer(post)

            if url_hyphens_replace(post_serializer.data['title']) != title:
                raise Http404()

            pagination = PaginationCreator(page, limit=6)
            offset = pagination.get_offset

            if f'post_viewed_{q_id}' not in request.session:
                Post.objects.filter(pk=q_id).update(post_views=F('post_views') + 1)
                request.session[f'post_viewed_{q_id}'] = True

            comments = Comment.objects.select_related(
                'user', 'post'
            ).prefetch_related(
                'likes', 'dislikes'
            ).annotate(
                likes_count=Count('likes'),
                dislikes_count=Count('dislikes')
            ).filter(post=post)[offset:offset + 6]

            comments_serializer = CommentSerializer(comments, many=True)
            context = {
                'post': post_serializer.data,
                'pages': post.comments_quantity,
                'current_user_image': image_serializer,
                'comments': sort_comments(order_by, comments_serializer)
            }
            cache.set(f'question.{q_id}.{title}.{order_by}.{page}', context, 120)
        else:
            context = cached_data
        return render(request, 'forum/forum_question_page.html',
                      context=context)

    @throttle_classes([UserRateThrottle])
    def create_comment(self, request, q_id: int, title: str):
        comment = request.POST.get('comment')
        comment = CommentSerializer(data={'comment': comment, 'post': q_id},
                                    context={'request': request})
        comment.is_valid(raise_exception=True)
        comment.save()

        delete_keys_matching_pattern(f'question.{q_id}*', f'profile.{request.user.id}*')
        return HttpResponseRedirect(f'/forum/question/{q_id}/{title}')

    @throttle_classes([UserRateThrottle])
    def create_post_rate(self, request, q_id: int, title: str):
        like = request.POST.get('like')
        dislike = request.POST.get('dislike')
        current_user: Request = request.user.id

        reactions_counters = Post.objects.prefetch_related('post_likes', 'post_dislikes').annotate(
            likes_counter=Count('post_likes'),
            dislikes_counter=Count('post_dislikes')
        ).get(pk=q_id)
        post_reactions_serializer = PostSerializer(reactions_counters)

        if like and not dislike:
            if current_user not in post_reactions_serializer.data['post_likes']:
                if current_user in post_reactions_serializer.data['post_dislikes']:
                    reactions_counters.post_dislikes.remove(current_user)
                else:
                    make_rate(request, reactions_counters.user, score=5)
                reactions_counters.post_likes.add(current_user)
        else:
            if current_user not in post_reactions_serializer.data['post_dislikes']:
                reactions_counters.post_likes.remove(current_user)
                reactions_counters.post_dislikes.add(current_user)

        delete_keys_matching_pattern(f'question.{q_id}*')
        return HttpResponseRedirect(f'/forum/question/{q_id}/{title}')

    @throttle_classes([UserRateThrottle])
    def create_comment_rate(self, request, q_id: int, title: str):
        like = request.POST.get('like')
        dislike = request.POST.get('dislike')
        comm_id = request.POST.get('comm_id')
        user_id = int(request.POST.get('user_id'))
        current_user: Request = request.user.id

        comment = Comment.objects.prefetch_related(
            'likes', 'dislikes'
        ).annotate(
            likes_counter=Count('likes'),
            dislikes_counter=Count('dislikes')
        ).get(pk=comm_id, post=q_id, user=user_id)
        comment_serializer = CommentSerializer(comment)

        if like and not dislike:
            if current_user not in comment_serializer.data['likes']:
                if current_user in comment_serializer.data['dislikes']:
                    comment.dislikes.remove(current_user)
                else:
                    make_rate(request, comment.user, score=10)
                comment.likes.add(current_user)
        else:
            if current_user not in comment_serializer.data['dislikes']:
                comment.likes.remove(current_user)
                comment.dislikes.add(current_user)

        delete_keys_matching_pattern(f'question.{q_id}*')
        return HttpResponseRedirect(f'/forum/question/{q_id}/{title}')

    @throttle_classes([UserRateThrottle])
    def delete_comment(self, request, q_id: int, title: str, comment_id: int):
        comment = Comment.objects.select_related('user').get(pk=comment_id)
        if comment.user.id == request.user.id:
            comment.delete()
        else:
            raise PermissionDenied()

        delete_keys_matching_pattern(f'question.{q_id}*', f'profile.{request.user.id}.*')
        return HttpResponseRedirect(f'/forum/question/{q_id}/{title}')


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
#         return render(request, 'forum/forum_base_page.html',
#                       context={'posts': posts,
#                                'page': pagination.get_page,
#                                'url': address_args,
#                                'current_user_image': image_serializer})
