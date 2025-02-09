from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.template import loader


def page_not_found(request, exception):
    template = loader.get_template("error/404.html")
    content = template.render()
    return HttpResponseNotFound(content, content_type="text/html")


def server_error(request, *args, **kwargs):
    template = loader.get_template("error/500.html")
    content = template.render()
    return HttpResponseServerError(content, content_type="text/html")


def unauthorized(request, *args, **kwargs):
    template = loader.get_template("error/401.html")
    content = template.render()
    return HttpResponse(content, content_type="text/html", status=401)
