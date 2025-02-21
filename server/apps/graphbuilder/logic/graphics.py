import matplotlib
import mpld3
import numpy as np
from django.views.generic import TemplateView
from matplotlib import pyplot as plt

from server.apps.graphbuilder.service import my_func

matplotlib.use('agg')


class GraphBuilderTemplateView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        function = self.request.GET.get('function')
        if function:
            fig = plt.figure()

            x_values = np.linspace(-10, 10, 100)
            y_values = my_func(x_values, function)

            plt.plot(x_values, y_values)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Графік функції {function}')

            html_graph = mpld3.fig_to_html(fig)
            context['graph'] = [html_graph]
        return context
