from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id: int, username: str):
        return render(request, 'forum/chat.html')
