from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.template import loader


def page_not_found(request, exception):
    template = loader.get_template('error/404.html')
    return HttpResponseNotFound(template.render())


def server_error(request, *args, **kwargs):
    template = loader.get_template('error/500.html')
    return HttpResponseServerError(template.render())


def unauthorized(request, *args, **kwargs):
    template = loader.get_template('error/401.html')
    return HttpResponse(template.render(), status=401)

