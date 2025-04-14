from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', include('server.urls.third_party_urls')),
    path(
        '',
        RedirectView.as_view(pattern_name='mathlab:math_news:base-math-news'),
        name='base-redirect',
    ),
    # nested apps urls
    path('mathlab/', include('server.urls.mathlab_urls')),  # this is the main app for math operations
    path('forum/', include('server.urls.forum_urls')),  # math forum
    path('theorist/onboarding/', include('server.apps.theorist.urls.onboarding_urls')),  # theorist onboarding urls
    path('', include('server.apps.users.urls')),  # for auth purposes
    path('exception/', include('server.urls.exception_urls')),  # convenient way to get exception in ajax
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
