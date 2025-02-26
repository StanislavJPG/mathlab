from django.contrib.auth.mixins import AccessMixin


class EmailVerifiedUsersMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
