from django.core.cache import cache
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from forum.utils import PaginationCreator
from math_news.models import MathNews
from math_news.serializers import NewsSerializer


def base_redirect(request):
    return redirect('base-math-news')


class NewsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        page = request.GET.get('page')
        cached_data = cache.get(f'news.page={page}', None)

        if not cached_data:
            pagination = PaginationCreator(page, limit=10)
            offset = pagination.get_offset

            all_news = MathNews.objects.all().order_by('-published_at')[offset:offset+10]
            news_serializer = NewsSerializer(all_news, many=True)
            context = {'all_news': news_serializer.data, 'page': page}
            cache.set(f'news.page={page}', context, 60*6)
        else:
            context = cached_data

        return render(request, 'base/index.html',
                      context=context)
