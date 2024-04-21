import os

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from forum.models import Post, Comment
from forum.serializers import PostSerializer, CommentLastActionsSerializer
from forum.utils import delete_keys_matching_pattern
from users.models import CustomUser as User, ProfileImage
from users.serializers import ProfileSerializer, UserSerializer


class Register(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'auth/registration.html')

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_by_email = User.objects.filter(email=email).first()
        user_by_name = User.objects.filter(username=username).first()

        if user_by_email or user_by_name:
            return render(request, 'auth/registration.html',
                          context={'error_msg': 'Користувач з цією поштою або нікнеймом вже зареєстрований.'})

        created_user = User.objects.create_user(username=username, email=email, password=password)
        Token.objects.create(user=created_user)

        auth_creds = authenticate(request, email=email, password=password)
        login(request, auth_creds)

        return HttpResponseRedirect(reverse('forum-base'))


class Login(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()

        if not user:
            return render(request, 'auth/login.html',
                          context={'error_msg': 'Цього користувача не існує.'})

        if not user.check_password(password):
            return render(request, 'auth/login.html',
                          context={'error_msg': 'Перевірте правильність введеного паролю.'})

        auth_creds = authenticate(request, email=email, password=password)
        login(request, auth_creds)

        return HttpResponseRedirect(reverse('forum-base'))


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)

        return render(request, 'auth/logout.html', context={'profile_image': image_serializer})

    def post(self, request):
        try:
            logout(request)
            cache.clear()
        finally:
            cache.exit()

        return HttpResponseRedirect(reverse('forum-base'))


class ResetPassword(SuccessMessageMixin, PasswordResetView):
    template_name = 'auth/password_reset.html'
    email_template_name = 'auth/password_reset_email.html'

    success_message = "Ми відправили вам інструкції щодо налаштування вашого пароля,"\
                      "якщо обліковий запис існує з введеною вами електронною адресою."\
                      "Ви повинні отримати їх незабаром."\
                      "Якщо ви не отримаєте електронного листа, будь ласка, переконайтеся,"\
                      "що ви ввели адресу, з якою зареєстровані, або ж перевірте папку Спам."

    success_url = reverse_lazy('forum-base')


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, user_id: int, username: str):
        try:
            cached_data = cache.get(f'profile.{user_id}.{username}')
            if not cached_data:
                user = User.objects.get(pk=user_id)
                posts_by_user = Post.objects.filter(user=user_id)[:7]
                comments_by_user = Comment.objects.filter(user=user_id)[:7]

                user_serializer = UserSerializer(user)
                post_serializer = PostSerializer(posts_by_user, many=True)
                comments_serializer = CommentLastActionsSerializer(comments_by_user, many=True)

                requested_user_image = ProfileSerializer.get_profile_image(user_pk=user_id)
                current_user_image = ProfileSerializer.get_profile_image(user_pk=request.user.id)

                all_actions = sorted(post_serializer.data + comments_serializer.data, key=lambda x: x['created_at'],
                                     reverse=True)
                context = {
                    'user_content': user_serializer.data,
                    'all_actions': all_actions,
                    'profile_image': requested_user_image,
                    'current_user_image': current_user_image
                }
                cache.set(f'profile.{user_id}.{username}', context, 120)
            else:
                context = cached_data

            return render(request, 'forum/user/profile.html',
                          context=context)
        except IndexError:
            raise Http404()

    def post(self, request, user_id: int, username: str):
        image = request.FILES['image']
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

        delete_keys_matching_pattern(['profile*', 'user_image*'])

        return HttpResponseRedirect(reverse('forum-profile', kwargs={'user_id': user_id, 'username': username}))
