from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import F, Q, Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import throttle_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import Request

from forum.elasticsearch.documents import PostDocument
from .models import Post, Category, Comment
from .serializers import PostSerializer, CommentSerializer
from .templatetags.filters import url_hyphens_replace
from .utils import PaginationCreator, sort_posts, sort_comments, delete_keys_matching_pattern, make_rate
from users.serializers import ProfileSerializer


class ForumBaseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        order_by = request.GET.get('sort')

        if order_by:
            page = request.GET.get('page')
            cached_data = cache.get(f'base_page.{page}.{order_by}', None)
            pagination = PaginationCreator(page, limit=10)
            offset = pagination.get_offset

            current_user_image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)

            if not cached_data:
                address_args = request.build_absolute_uri().split('/')[-1].split('page=')[0] + 'page='
                context = {
                    'page': pagination.get_page,
                    'url': address_args,
                    'current_user_image': current_user_image_serializer
                }

                posts = Post.objects.select_related('user').prefetch_related(
                    'post_likes', 'post_dislikes', 'categories')[offset:offset + 10]
                post_serializer = PostSerializer(posts, many=True)

                context['posts'] = sort_posts(order_by, post_serializer, offset)
                cache.set(f'base_page.{page}.{order_by}', context, 120)
            else:
                context = cached_data

            return render(request, 'forum/forum_base_page.html',
                          context=context)

        return HttpResponseRedirect('/forum/?sort=popular&page=1')

    @throttle_classes([UserRateThrottle])
    def post(self, request):
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


class QuestionCreationView(APIView):
    permission_classes = [IsAuthenticated]
    categories = ('Графіки функцій', 'Матриці', 'Рівняння', 'Нерівності',
                  'Системи', 'Вища математика', 'Теорії ймовірностей',
                  'Комбінаторика', 'Дискретна математика', 'Початкова математика', 'Відсотки',
                  'Тригонометрія', 'Геометрія', 'Ймовірність і статистика', 'Алгоритми', 'Інше', 'Алгебра')

    def get(self, request):
        image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)
        return render(request, 'forum/forum_add_question_page.html',
                      context={
                          'categories': enumerate(self.categories, start=1),
                          'current_user_image': image_serializer
                      })

    @throttle_classes([UserRateThrottle])
    def post(self, request):
        title = request.POST.get('title')
        requested_categories = [int(c) for c in request.POST.getlist('category')]
        content = request.POST.get('content')
        context = {'categories': enumerate(self.categories, start=1)}

        if len(requested_categories) > 4 or len(requested_categories) < 1:
            context['error_msg'] = 'Менше однієї, або більше чотирьох категорій не приймається.'

            return render(request, 'forum/forum_add_question_page.html',
                          context=context)

        post_creation = Post.objects.create(title=title, content=content, user=request.user)
        categories = Category.objects.filter(pk__in=requested_categories)

        post_creation.categories.add(*categories)
        post_creation.save()
        delete_keys_matching_pattern('base_page*')

        created_post = (Post.objects.select_related('user').prefetch_related(
            'post_likes', 'post_dislikes', 'categories').order_by('-created_at')[:1]
                        .values('id', 'title').get())

        post_title = url_hyphens_replace(created_post['title'])

        return HttpResponseRedirect(f'/forum/question/{created_post["id"]}/{post_title}')


class QuestionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, q_id: int, title: str):
        order_by = request.GET.get('order_by')
        cached_data = cache.get(f'question.{q_id}.{title}.{order_by}', None)
        page = request.GET.get('page')

        if not cached_data:
            image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)

            post = Post.objects.select_related('user').prefetch_related('categories', 'post_likes', 'post_dislikes'
                                                                        ).get(pk=q_id)
            post_serializer = PostSerializer(post)

            if url_hyphens_replace(post_serializer.data['title']) != title:
                raise Http404()

            pagination = PaginationCreator(page, limit=6)
            offset = pagination.get_offset

            if f'post_viewed_{q_id}' not in request.session:
                Post.objects.filter(pk=q_id).update(post_views=F('post_views') + 1)
                request.session[f'post_viewed_{q_id}'] = True

            context = {
                'post': post_serializer.data,
                'pages': Comment.objects.filter(post=post).count(),
                'current_user_image': image_serializer
            }

            comments = Comment.objects.select_related('user', 'post'
                                                      ).prefetch_related('likes', 'dislikes'
                                                      ).filter(post=post)[offset:offset + 6]
            comments_serializer = CommentSerializer(comments, many=True)

            context['comments'] = sort_comments(order_by, comments_serializer)
            cache.set(f'question.{q_id}.{title}.{order_by}', context, 120)
        else:
            context = cached_data
        return render(request, 'forum/forum_question_page.html',
                      context=context)

    @throttle_classes([UserRateThrottle])
    def create_comment(self, request, q_id: int, title: str):
        comment = request.POST.get('comment')

        if len(comment) >= 15:
            post = Post.objects.select_related('user').get(Q(pk=q_id) & Q(user=request.user.id))
            Comment.objects.create(comment=comment, post=post, user=post.user)

            delete_keys_matching_pattern(f'question.{q_id}*', f'profile.{request.user.id}*')
        return HttpResponseRedirect(f'/forum/question/{q_id}/{title}')

    @throttle_classes([UserRateThrottle])
    def create_post_rate(self, request, q_id: int, title: str):
        like = request.POST.get('like')
        dislike = request.POST.get('dislike')

        reactions_counters = Post.objects.prefetch_related('post_likes', 'post_dislikes').annotate(
            likes_counter=Count('post_likes'),
            dislikes_counter=Count('post_dislikes')
        ).get(pk=q_id)

        if like and not dislike:
            if reactions_counters.likes_counter == 1:
                ...
            elif reactions_counters.likes_counter == 0 and reactions_counters.dislikes_counter == 1:
                reactions_counters.post_dislikes.remove(request.user.id)
            else:
                make_rate(request, reactions_counters.user, score=5)

            reactions_counters.post_likes.add(request.user.id)

        else:
            if reactions_counters.dislikes_counter == 1:
                ...
            elif reactions_counters.dislikes_counter == 0 and reactions_counters.likes_counter == 1:
                reactions_counters.post_likes.remove(request.user.id)

            reactions_counters.post_dislikes.add(request.user.id)

        delete_keys_matching_pattern(f'question.{q_id}*')
        return HttpResponseRedirect(f'/forum/question/{q_id}/{title}')

    @throttle_classes([UserRateThrottle])
    def create_comment_rate(self, request, q_id: int, title: str):
        like = request.POST.get('like')
        dislike = request.POST.get('dislike')
        comm_id = request.POST.get('comm_id')
        user_id = int(request.POST.get('user_id'))
        curr_user: Request = request.user.id

        comments = Comment.objects.prefetch_related(
            'likes', 'dislikes'
        ).annotate(
            likes_by_current_user=Count('likes'),
            dislikes_by_current_user=Count('dislikes')
        ).get(pk=comm_id, post=q_id, user=user_id)

        if like and not dislike:
            if comments.likes_by_current_user == 1:
                ...
            elif comments.likes_by_current_user == 0 and comments.dislikes_by_current_user == 1:
                comments.dislikes.remove(curr_user)
            else:
                make_rate(request, user_id, score=10)

            comments.likes.add(curr_user)

        else:
            if comments.dislikes_by_current_user == 1:
                ...
            elif comments.dislikes_by_current_user == 0 and comments.likes_by_current_user == 1:
                comments.likes.remove(curr_user)

            comments.dislikes.add(curr_user)

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


class PostSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        search_pattern = request.GET.get('search_pattern')
        page = request.GET.get('page')

        pagination = PaginationCreator(page, limit=10)
        offset = pagination.get_offset

        address_args = request.build_absolute_uri().split('/')[-1].split('page=')[0] + 'page='
        image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)
        cached_data = cache.get(f'base_page.search.{search_pattern}.{page}')

        if not cached_data:
            post = PostDocument().search().query("match", title=search_pattern)[offset:offset+10]
            post_queryset = post.to_queryset()
            post_serializer = PostSerializer(post_queryset, many=True)

            posts = sort_posts('newest', post_serializer, offset)
            cache.set(f'base_page.search.{search_pattern}.{page}', posts, 120)
        else:
            posts = cached_data

        return render(request, 'forum/forum_base_page.html',
                      context={'posts': posts,
                               'page': pagination.get_page,
                               'url': address_args,
                               'current_user_image': image_serializer})
