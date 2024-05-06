from django.core.cache import cache
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from forum.utils import make_offset
from math_news.models import MathNews
from math_news.serializers import NewsSerializer


def base_redirect(request):
    return redirect('base-math-news')


class NewsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            page = int(request.GET.get('page'))
        except TypeError:
            page = 1
        cached_data = cache.get(f'news.page={page}', None)

        if not cached_data:
            offset = make_offset(page, limit=10)
            all_news = MathNews.objects.all().order_by('-published_at')[offset:offset+10]
            news_serializer = NewsSerializer(all_news, many=True)
            context = {'all_news': news_serializer.data, 'page': page}
            cache.set(f'news.page={page}', context, 60*6)
        else:
            context = cached_data

        return render(request, 'base/index.html',
                      context=context)
