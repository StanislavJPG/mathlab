from django.views.generic import DetailView

from server.apps.game_area.logic.quizzes.context_builder import MathQuizContextBuilder


class MathQuizContextBuilderViewMixin(DetailView):
    context_builder = MathQuizContextBuilder

    def get_context_builder(self):
        return self.context_builder(self.get_object(), self.get_queryset(), self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_builder = self.get_context_builder()
        context_builder.get_context_data(context)
        return context
