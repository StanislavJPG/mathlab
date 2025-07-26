import matplotlib
import mpld3
import numpy as np
from django.utils.html import format_html
from render_block import render_block_to_string
from latex2sympy2 import latex2sympy
from sympy import lambdify, symbols
from braces.views import FormInvalidMessageMixin
from django.http import HttpResponse
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

            x = symbols('x')
            sym_expr = latex2sympy(function)

            f = lambdify(x, sym_expr, modules=['numpy'])

            x_vals = np.linspace(-10, 10, 100)
            y_vals = f(x_vals)
            if np.isscalar(y_vals):
                y_vals = np.full_like(x_vals, y_vals)

            plt.plot(x_vals, y_vals, label=function)
            plt.xlabel('x')
            plt.ylabel('y')

            html_graph = mpld3.fig_to_html(fig)

            context = {'graph': html_graph}
            block_form = render_block_to_string(self.template_name, 'graph_block', context, request=self.request)
            return HttpResponse(content=block_form)

        return self._render_error()

    def _render_error(self):
        message = self.get_form_invalid_message()
        self.messages.error(message, fail_silently=True)
        html_error_msg = format_html(
            f"""
            <div class="alert alert-danger mt-4" role="alert">
              {message}
            </div>
            """
        )
        block_form = render_block_to_string(
            self.template_name, 'graph_block', {'graph': html_error_msg}, request=self.request
        )
        return HttpResponse(content=block_form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GraphBuilderForm()
        return context
