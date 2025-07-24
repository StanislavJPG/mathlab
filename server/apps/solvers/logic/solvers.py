import matplotlib
import mpld3
import numpy as np
from braces.views import FormInvalidMessageMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from matplotlib import pyplot as plt

from server.apps.solvers.forms import GraphBuilderForm

matplotlib.use('agg')


class EquationsTemplateView(TemplateView):
    """Maybe in the future, will make this functionality only for auth users or only for paid."""

    template_name = 'partials/equations.html'


class GraphBuilderTemplateView(FormInvalidMessageMixin, TemplateView):
    template_name = 'partials/graphbuilder.html'
    form_invalid_message = _('Error. Please, check your input and try again.')

    def post(self, request, *args, **kwargs):
        function = request.POST['function']
        form = GraphBuilderForm(data={'function': function})
        if form.is_valid():
            fig = plt.figure()

            x_values = np.linspace(-10, 10, 100)
            y_values = eval(function, {'x': x_values, 'np': np})

            plt.plot(x_values, y_values)
            plt.xlabel('x')
            plt.ylabel('y')

            html_graph = mpld3.fig_to_html(fig)

            context = {**self.get_context_data(), 'form': form, 'graph': [html_graph]}
            block_form = render_to_string(self.template_name, context, request=self.request)
            return HttpResponse(content=block_form)
        else:
            self.messages.error(self.request, self.get_form_invalid_message())
            return HttpResponse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GraphBuilderForm()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     function = self.request.GET.get('function')
    #     if function:
    #
    #     return context
