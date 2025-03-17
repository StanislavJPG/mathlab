from django.views.generic import ListView

from server.apps.carousel.models import Carousel
from server.common.mixins.views import HXViewMixin


class CarouselBaseListView(HXViewMixin, ListView):
    model = Carousel
    context_object_name = 'carousels'
    template_name = 'carousel.html'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
