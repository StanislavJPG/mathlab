from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from forum.models import Post, Category, Comment
from forum.serializers import PostSerializer, CommentSerializer
from users.models import CustomUser as User
from users.serializers import UserSerializer


class ForumBaseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        page = int(request.GET.get('page', 1))
        sort = request.GET.get('sort')

        if page and sort:
            # if url has an arguments
            address_args = request.build_absolute_uri().split('/')[4][0:-1]

            if page > 0:
                offset = (page - 1) * 10
            else:
                raise Http404()

            if sort == 'last-week':
                end_date = timezone.now()
                start_date = end_date - timedelta(days=7)
                posts = Post.objects.filter(created_at__gte=start_date, created_at__lt=end_date
                                            ).order_by('-created_at')[offset:offset + 10]
                serializer = PostSerializer(posts, many=True)

                return render(request, 'forum/forum_base_page.html',
                              context={
                                  'posts': serializer.data,
                                  'page': page,
                                  'url': address_args
                              })

            if sort == 'popular':
                # maybe add comments later///////
                # sort_by = '-likes'
                sort_by = '-created_at'

            elif sort == 'interest':
                # sort_by = '-likes'
                sort_by = '-created_at'

            elif sort == 'newest':
                sort_by = '-created_at'

            else:
                raise Http404()

            posts = Post.objects.all().order_by(sort_by)[offset:offset + 10]
            serializer = PostSerializer(posts, many=True)

            return render(request, 'forum/forum_base_page.html',
                          context={
                              'posts': serializer.data,
                              'page': page,
                              'url': address_args
                          })
        return HttpResponseRedirect('/forum/?sort=popular&page=1')


def forum_topics(request):
    return render(request, 'forum/forum_topics_page.html')


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, user_id: int, username: str):
        try:
            user = User.objects.filter(pk=user_id)
            user_serializer = UserSerializer(user, many=True)

            return render(request, 'forum/user/profile.html',
                          context={'user_content': user_serializer.data[0]})
        except IndexError:
            raise Http404()

    def post(self, request):
        ...


class QuestionCreationView(APIView):
    permission_classes = [IsAuthenticated]
    categories = ('Графіки функцій', 'Матриці', 'Рівняння', 'Нерівності',
                  'Системи', 'Вища математика', 'Теорії ймовірностей',
                  'Комбінаторика', 'Дискретна математика', 'Початкова математика', 'Відсотки',
                  'Тригонометрія', 'Геометрія', 'Ймовірність і статистика', 'Алгоритми', 'Інше')

    def get(self, request):
        return render(request, 'forum/forum_add_question_page.html',
                      context={'categories': enumerate(self.categories, start=1)})

    def post(self, request):
        title = request.POST.get('title')
        requested_categories = [int(c) for c in request.POST.getlist('category')]
        content = request.POST.get('content')
        context = {'categories': enumerate(self.categories, start=1)}

        if len(requested_categories) > 4 or len(requested_categories) < 1:
            context['error_msg'] = 'Менше однієї, або більше чотирьох категорій не приймається.'

            return render(request, 'forum/forum_add_question_page.html',
                          context=context)

        user = get_object_or_404(get_user_model(), id=request.user.id)

        post_creation = Post.objects.create(title=title, content=content, user=user)
        categories = Category.objects.filter(pk__in=requested_categories)

        post_creation.categories.add(*categories)
        post_creation.save()

        return HttpResponseRedirect('/forum/?sort=newest&page=1')


class QuestionView(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, q_id: int, title: str):
        try:
            page = int(request.GET.get('page'))
        except TypeError:
            page = 1

        if page > 0:
            offset = (page - 1) * 6
        else:
            raise Http404()

        if 'post_viewed_{}'.format(q_id) not in request.session:
            Post.objects.filter(pk=q_id).update(post_views=F('post_views') + 1)
            request.session['post_viewed_{}'.format(q_id)] = True

        post = Post.objects.get(pk=q_id)
        comments = Comment.objects.filter(post=post).order_by('created_at')[offset:offset+6]

        post_serializer = PostSerializer(post)
        comments_serializer = CommentSerializer(comments, many=True)

        return render(request, 'forum/forum_question_page.html',
                      context={
                          'post': post_serializer.data,
                          'comments': comments_serializer.data,
                          'pages': len(Comment.objects.filter(post=post)),
                      })

    def create_comment(self, request, q_id: int, title: str):
        comment = request.POST.get('comment')

        if len(comment) >= 15:
            user = get_object_or_404(get_user_model(), pk=request.user.id)
            post = get_object_or_404(Post, pk=q_id)

            comm_creation = Comment.objects.create(comment=comment, post=post, user=user)
            comm_creation.save()

        return HttpResponseRedirect(f'/forum/question/{q_id}/{title}')

    def create_rate(self, request, q_id: int, title: str):
        like = request.POST.get('like')
        dislike = request.POST.get('dislike')
        post = Post.objects.get(pk=q_id)

        likes_counter = post.post_likes.filter(pk=request.user.id).count()
        dislikes_counter = post.post_dislikes.filter(pk=request.user.id).count()

        if like and not dislike:
            if likes_counter == 1:
                ...
            elif likes_counter == 0 and dislikes_counter == 1:
                post.post_dislikes.remove(request.user.id)

            post.post_likes.add(request.user.id)

        else:
            if dislikes_counter == 1:
                ...
            elif dislikes_counter == 0 and likes_counter == 1:
                post.post_likes.remove(request.user.id)

            post.post_dislikes.add(request.user.id)

        return HttpResponseRedirect(f'/forum/question/{q_id}/{title}')
