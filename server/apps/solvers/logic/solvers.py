import matplotlib
from django.views.generic import TemplateView

from server.apps.solvers.forms import GraphBuilderForm

matplotlib.use('agg')


class EquationsTemplateView(TemplateView):
    """Maybe in the future, will make this functionality only for auth users or only for paid."""

    template_name = 'partials/equations.html'


class GraphBuilderTemplateView(TemplateView):
    template_name = 'partials/graphbuilder.html'

    def post(self, request, *args, **kwargs):
        function = request.POST['function']  # noqa: F841
        # form = GraphBuilderForm(data={'function': function})
        # if form.is_valid():
        #     print(function, form)
        #     return HttpResponse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GraphBuilderForm()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     function = self.request.GET.get('function')
    #     if function:
    #         fig = plt.figure()
    #
    #         x_values = np.linspace(-10, 10, 100)
    #         y_values = my_func(x_values, function)
    #
    #         plt.plot(x_values, y_values)
    #         plt.xlabel('x')
    #         plt.ylabel('y')
    #         plt.title(f'Графік функції {function}')
    #
    #         html_graph = mpld3.fig_to_html(fig)
    #         context['graph'] = [html_graph]
    #     return context
