from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from forum.utils import make_offset
from math_news.models import MathNews
from math_news.serializers import NewsSerializer


class NewsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        offset = make_offset(request, limit=10)
        all_news = MathNews.objects.all()[offset:offset+10]
        news_serializer = NewsSerializer(all_news, many=True)

        return render(request, 'base/index.html', context={'all_news': news_serializer.data})
