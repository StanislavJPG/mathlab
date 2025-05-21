from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, UpdateView
from django_htmx.http import HttpResponseClientRedirect

from server.apps.theorist.forms import TheoristOnboardForm
from server.apps.theorist.models import Theorist
from server.common.mixins.views import HXViewMixin


class TheoristOnboardingTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'onboarding.html'

    def dispatch(self, request, *args, **kwargs):
        if request.theorist.is_onboarded:
            return redirect(reverse('forum:base-forum-page'))
        return super().dispatch(request, *args, **kwargs)


class HXTheoristOnboardFormView(LoginRequiredMixin, FormMessagesMixin, HXViewMixin, UpdateView):
    model = Theorist
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_class = TheoristOnboardForm
    template_name = 'partials/onboarding_form.html'
    form_valid_message = _('You successfully registered!')
    form_invalid_message = _('Error. Please, check your input and try again.')
    success_url = reverse_lazy('forum:base-forum-page')

    def form_valid(self, form):
        super().form_valid(form)
        response = HttpResponseClientRedirect(reverse('forum:base-forum-page'))
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return response
