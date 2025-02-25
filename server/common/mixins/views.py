from django.contrib.auth.mixins import AccessMixin
from django.db import transaction


class EmailVerifiedUsersMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class RaiseScoreMixin:
    def _relation_by_request_param(self):
        from server.apps.forum.models import support

        self.object = self.get_object()
        relation_map = {}
        for relation in support.__all__:
            name_without_suffix = relation.removesuffix('Support').lower()
            relation_class = getattr(support, relation)
            relation_map.update(
                {
                    name_without_suffix: (relation_class, name_without_suffix),
                }
            )

        model_class, field_name = relation_map[self.kwargs['model']]
        related_model = model_class._meta.get_field(field_name).related_model
        related_instance = related_model.objects.filter(uuid=self.kwargs['model_uuid']).first()

        if not related_instance:
            return None

        with transaction.atomic():
            obj, created = model_class.objects.get_or_create(theorist=self.object, **{field_name: related_instance})

            if created:
                self.object.add_max_score()

            return obj
