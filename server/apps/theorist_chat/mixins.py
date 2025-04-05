from server.common.http import AuthenticatedHttpRequest


class ChatConfigurationRequiredMixin:
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        if self.request.theorist and not self.request.theorist.chat_configuration.is_chats_available:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
