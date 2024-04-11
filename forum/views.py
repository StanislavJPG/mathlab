from django.shortcuts import render


def forum_base(request):
    return render(request, 'forum/forum_base_page.html')


def forum_topics(request):
    return render(request, 'forum/forum_topics_page.html')
