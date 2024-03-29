from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')


def server_error(request, *args, **kwargs):
    return HttpResponseServerError(request, 'error/500.html')
