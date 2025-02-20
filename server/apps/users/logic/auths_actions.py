from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from rest_framework.views import APIView

from server.apps.users.models import CustomUser as User


class Register(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "auth/registration.html")

    def post(self, request):
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user_by_email = User.objects.filter(email=email).first()
        user_by_name = User.objects.filter(username=username).first()

        if user_by_email or user_by_name:
            return render(
                request,
                "auth/registration.html",
                context={
                    "error_msg": "Користувач з цією поштою або нікнеймом вже зареєстрований."
                },
            )

        created_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        Token.objects.create(user=created_user)

        auth_creds = authenticate(request, email=email, password=password)
        login(request, auth_creds)

        return HttpResponseRedirect(reverse("base-redirect"))


class Login(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(email=email).first()

        if not user:
            return render(
                request,
                "auth/login.html",
                context={"error_msg": "Цього користувача не існує."},
            )

        if not user.check_password(password):
            return render(
                request,
                "auth/login.html",
                context={"error_msg": "Перевірте правильність введеного паролю."},
            )

        auth_creds = authenticate(request, email=email, password=password)
        login(request, auth_creds)
        cache.clear()

        return HttpResponseRedirect(reverse("base-redirect"))


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)

        return render(
            request,
            "auth/logout.html",
        )

    def post(self, request):
        logout(request)
        cache.clear()

        return HttpResponseRedirect(reverse("base-redirect"))


class ResetPassword(SuccessMessageMixin, PasswordResetView):
    template_name = "auth/password_reset.html"
    email_template_name = "auth/password_reset_email.html"

    success_message = (
        "Ми відправили вам інструкції щодо налаштування вашого пароля,"
        "якщо обліковий запис існує з введеною вами електронною адресою."
        "Ви повинні отримати їх незабаром."
        "Якщо ви не отримаєте електронного листа, будь ласка, переконайтеся,"
        "що ви ввели адресу, з якою зареєстровані, або ж перевірте папку Спам."
    )

    success_url = reverse_lazy("base-redirect")
