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
        field_name='categories__name',
        to_field_name='name',
        queryset=PostCategory.objects.all(),
    )
    sort_by = filters.OrderingFilter(
        label=_('Sort by'),
        choices=(
            ('-likes_counter', _('Likes quantity')),
            ('-comments_quantity', _('Comments quantity')),
            ('-hit_count_generic__hits', _('Posts views')),
        ),
    )

    class Meta:
        model = Post
        fields = ('title', 'categories')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['categories'].field.label_from_instance = lambda obj: obj.get_name_display()
