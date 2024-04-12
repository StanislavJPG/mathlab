from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


def forum_base(request):
    return render(request, 'forum/forum_base_page.html')


def forum_topics(request):
    return render(request, 'forum/forum_topics_page.html')


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'forum/user/profile.html')

    def post(self, request):
        ...


class QuestionCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'forum/forum_add_question_page.html')

    def post(self, request):
        ...
