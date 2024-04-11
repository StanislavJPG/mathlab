from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import renderers
from rest_framework.views import APIView as GeneralAPIView

from users.models import CustomUser as User


class APIView(GeneralAPIView):
    renderer_classes = [renderers.HTMLFormRenderer]


class Register(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'auth/registration.html')

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()

        if user:
            raise AuthenticationFailed('User with that email is already exists.')

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
            raise AuthenticationFailed('User is not exists.')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is not correct.')

        auth_creds = authenticate(request, email=email, password=password)
        login(request, auth_creds)

        return HttpResponseRedirect(reverse('forum-base'))


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'auth/logout.html')

    def post(self, request):
        logout(request)

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

