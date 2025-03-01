from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden


class EmailVerifiedUsersMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OnlyOwnerChangesMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        theorist = self.get_object()
        if request.method in ['POST', 'PATCH', 'PUT'] and theorist != request.theorist:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
