from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from server.apps.game_area.forms import MathQuizFinishForm
from server.apps.game_area.models import MathQuiz


class MathQuizFinishDetailView(CreateView):
    model = MathQuiz
    form_class = MathQuizFinishForm
    template_name = 'quizzes/base_quiz.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('mathlab:gamearea:quizzes:mathquiz-base', args=[self.get_object().uuid]))
