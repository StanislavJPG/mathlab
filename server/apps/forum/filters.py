import django_filters as filters

from django.utils.translation import gettext_lazy as _

from server.apps.forum.models import Post, PostCategory


class PostListFilter(filters.FilterSet):
    title = filters.CharFilter(
        label=_('Title'),
        lookup_expr='icontains',
    )
    categories = filters.ModelMultipleChoiceFilter(
        label=_('Categories'),
        field_name='categories',
        to_field_name='id',
        queryset=PostCategory.objects.all(),
    )

    class Meta:
        model = Post
        fields = ('title', 'categories')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['categories'].field.label_from_instance = lambda obj: obj.get_name_display()
