from boringavatars import avatar
from django.http import HttpResponse
from django.views.generic import DetailView

from server.common.third_party_apps.boringavatar import BORINGAVATARS_DEFAULT_COLORS


class AvatarDetailViewMixin(DetailView):
    unique_avatar_field = None  # this is unique identifier of instance to render avatar

    def _get_nested_attr(self, obj, attr, default=None):
        for part in attr.split('.'):
            obj = getattr(obj, part, default)
            if obj is default:
                return default
        return obj

    def get_unique_avatar_field(self):
        self.object = self.get_object()
        if self.unique_avatar_field is None:
            raise NotImplementedError(f'You have to set `unique_avatar_field` by {self.model.__name__} model field.')

        if '__' in self.unique_avatar_field:
            self.unique_avatar_field = self.unique_avatar_field.replace('__', '.')
            return self._get_nested_attr(self.object, self.unique_avatar_field)

        if not hasattr(self.object, self.unique_avatar_field):
            raise NotImplementedError(
                f'Specified `unique_avatar_field` field does not exists in {self.model.__name__} model.'
            )

        return getattr(self.object, self.unique_avatar_field)

    def get(self, request, *args, **kwargs):
        name = self.get_unique_avatar_field()
        return HttpResponse(
            avatar(
                name=name,
                variant='beam',
                colors=BORINGAVATARS_DEFAULT_COLORS,
                square=False,
            ),
            content_type='image/svg+xml',
        )
