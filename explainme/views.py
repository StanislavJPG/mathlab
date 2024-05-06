from django.core.cache import cache
from django.shortcuts import render

from explainme.scraper import ExplainmeScraper


async def explain_me(request):
    topic = request.GET.get('topic', '')
    if not topic:
        context = {}

    else:
        cached_data = cache.get(f'explainme.{topic}')
        if not cached_data:
            user_request = ExplainmeScraper(topic)
            explanation = await user_request.get_description()
            img = await user_request.get_image()

            context = {'explanation': explanation, 'img': img}
            cache.set(f'explainme.{topic}', context, 180)
        else:
            context = cached_data

    return render(request, 'explainme/index.html', context=context)
