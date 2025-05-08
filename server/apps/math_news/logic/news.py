from django.views.generic import TemplateView, ListView

from server.apps.math_news.models import MathNews
from server.common.mixins.views import HXViewMixin


class NewsBaseTemplateView(TemplateView):
    template_name = 'news_base.html'


class NewsListView(HXViewMixin, ListView):
    model = MathNews
    template_name = 'partials/news_list.html'
    context_object_name = 'news'
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter_by_is_visible()
