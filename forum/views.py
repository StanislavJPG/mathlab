from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from forum.models import Post, Category, Comment
from forum.serializers import PostSerializer
from users.models import CustomUser as User
from users.serializers import UserSerializer


class ForumBaseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')[:5]
        serializer = PostSerializer(posts, many=True)

        return render(request, 'forum/forum_base_page.html',
                      context={
                          'posts': serializer.data
                      })


def forum_topics(request):
    return render(request, 'forum/forum_topics_page.html')


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, user_id):
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

    def get(self, request):
        categories = ('Графіки функцій', 'Матриці', 'Рівняння', 'Нерівності',
                      'Системи', 'Вища математика', 'Теорії ймовірностей',
                      'Комбінаторика', 'Дискретна математика', 'Початкова математика', 'Відсотки',
                      'Тригонометрія', 'Геометрія', 'Ймовірність і статистика', 'Алгоритми', 'Інше')

        return render(request, 'forum/forum_add_question_page.html',
                      context={'categories': enumerate(categories, start=1)})

    def post(self, request):
        title = request.POST.get('title')
        requested_categories = [int(c) for c in request.POST.getlist('category')]
        content = request.POST.get('content')

        if len(requested_categories) > 4:
            form = QuestionCreationView()
            return render(request, 'forum/forum_add_question_page.html', context={'form': form})
            # raise BadRequest('More than 4 choices is not accepts.')

        user = get_object_or_404(get_user_model(), id=request.user.id)

        post_creation = Post.objects.create(title=title, content=content, user=user)
        categories = Category.objects.filter(pk__in=requested_categories)

        post_creation.categories.add(*categories)
        post_creation.save()

        return HttpResponseRedirect(reverse('forum-base'))

