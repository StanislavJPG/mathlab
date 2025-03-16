from django.urls import path

from server.apps.carousel.logic.carousel import CarouselBaseListView

app_name = 'carousel'

urlpatterns = [
    path('hx-base-list/', CarouselBaseListView.as_view(), name='hx-base-list'),
]
