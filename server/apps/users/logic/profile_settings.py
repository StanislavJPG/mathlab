from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView

from server.apps.users.models import CustomUser as User


class TheoristSettingsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(
            request,
            'forum/settings.html',
        )

    def post(self, request):
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        user = User.objects.get(
            username=request.user.username, email=request.user.email
        )

        if new_username and new_username != user.username:
            if (
                User.objects.filter(username=new_username)
                .exclude(email=user.email)
                .exists()
            ):
                error_msg = {
                    'error_msg': 'Користувач з даним нікнеймом вже зареєстрований.'
                }
                return render(request, 'forum/settings.html', context=error_msg)
            user.username = new_username

        elif new_email and new_email != user.email:
            if (
                User.objects.filter(email=new_email)
                .exclude(username=user.username)
                .exists()
            ):
                error_msg = {
                    'error_msg': 'Користувач з даною поштою вже зареєстрований.'
                }
                return render(request, 'forum/settings.html', context=error_msg)
            user.email = new_email

        else:
            error_msg = {'error_msg': 'Заповніть поля, які хочете змінити.'}
            return render(request, 'forum/settings.html', context=error_msg)

        user.save()
        return HttpResponseRedirect(reverse('forum-settings'))
