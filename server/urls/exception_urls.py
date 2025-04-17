from django.urls import path
from django.views.generic import TemplateView

app_name = 'exception'

urlpatterns = [
    path(
        'hx/404/',
        TemplateView.as_view(template_name='alerts/not_found_alert.html', extra_context={'msg': ''}),
        name='hx-404',
    ),
    path(
        'hx/401/',
        TemplateView.as_view(template_name='alerts/only_for_authenticated.html'),
        name='hx-401',
    ),
]
