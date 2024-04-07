import matplotlib
import mpld3
import numpy as np
from django.shortcuts import render
from matplotlib import pyplot as plt

from graphbuilder.service import my_func

matplotlib.use('agg')


def index(request):
    function = request.GET.get('function')
    if function:
        fig = plt.figure()

        x_values = np.linspace(-10, 10, 100)
        y_values = my_func(x_values, function)

        plt.plot(x_values, y_values)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Графік функції {function}')

        html_graph = mpld3.fig_to_html(fig)
        context = {'graph': [html_graph]}
    else:
        context = {}

    return render(request=request, template_name='graphbuilder/index.html',
                  context=context)
