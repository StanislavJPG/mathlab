from django.shortcuts import render
from django.http import HttpResponseNotFound


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')
