from django.views.generic import TemplateView


class ChatView(TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_uuid'] = self.kwargs['uuid']
        return context
