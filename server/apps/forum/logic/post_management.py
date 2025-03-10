from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, CreateView, DeleteView
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event

from server.apps.forum.forms import PostCreateForm
from server.apps.forum.models import Post
from server.common.http import AuthenticatedHttpRequest


class PostCreateBaseView(LoginRequiredMixin, TemplateView):
    template_name = 'posts/create_question_page.html'


class PostCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    model = Post
    template_name = 'posts/partials/create_question_form.html'
    form_class = PostCreateForm
    form_valid_message = _('You successfully created a new post.')
    form_invalid_message = _('Error while creating post. Please check for errors and try again.')

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        return kwargs

    def form_valid(self, form):
        post = form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        response = HttpResponseClientRedirect(post.get_absolute_url())
        return response


class PostDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    model = Post
    form_valid_message = _('Your post has been deleted.')
    form_invalid_message = _('Error. Please, check your input and try again.')
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()

        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        if self.kwargs['location'] == 'base':
            response = HttpResponse()
            trigger_client_event(response, 'postDeleted')
        else:
            response = HttpResponseClientRedirect(reverse('forum:base-forum-page'))

        return response
