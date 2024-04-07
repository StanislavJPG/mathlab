import asyncio

from django.shortcuts import render

from explainme.scraper import ExplainmeScraper


async def index(request):
    topic = request.GET.get('topic', '')

    if topic:
        topic = ExplainmeScraper(topic)
        explanation = await topic.get_description()
        img = await topic.get_image()

        context = {'explanation': explanation, 'img': img}
    else:
        context = {}

    return render(request, 'explainme/index.html', context=context)


