from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from users.models import CustomUser as User


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

        return HttpResponseRedirect('/solvexample/equations')


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

        return HttpResponseRedirect('/solvexample/equations')


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'auth/logout.html')

    def post(self, request):
        logout(request)

        return HttpResponseRedirect('/solvexample/equations')



