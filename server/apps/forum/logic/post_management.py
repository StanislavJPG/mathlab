from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event

from server.apps.forum.forms.posts import PostCreateForm, PostUpdateForm
from server.apps.forum.models import Post
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class PostCreateBaseView(LoginRequiredMixin, TemplateView):
    template_name = 'posts/create_question_page.html'


class PostCreateView(HXViewMixin, LoginRequiredMixin, FormMessagesMixin, CreateView):
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


class PostContentUpdateView(HXViewMixin, LoginRequiredMixin, FormMessagesMixin, UpdateView):
    model = Post
    template_name = 'posts/partials/post_content_update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_class = PostUpdateForm
    form_valid_message = _('Your post has been updated.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().filter(theorist=self.request.theorist)

    def form_valid(self, form):
        form = form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        # use redirect instead of refresh to save toasts because of HX-Redirect header
        response = HttpResponseClientRedirect(form.get_absolute_url())
        return response


class PostTitleUpdateView(HXViewMixin, LoginRequiredMixin, FormMessagesMixin, UpdateView):
    model = Post
    template_name = 'posts/partials/post_title_update.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    fields = ('title',)
    form_valid_message = _('Your post has been updated.')
    form_invalid_message = _('Error. Please, check your input and try again.')

    def get_queryset(self):
        self.request: AuthenticatedHttpRequest
        return super().get_queryset().filter(theorist=self.request.theorist)

    def form_valid(self, form):
        form = form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        # use redirect instead of refresh to save toasts because of HX-Redirect header
        response = HttpResponseClientRedirect(form.get_absolute_url())
        return response


class PostDeleteView(HXViewMixin, LoginRequiredMixin, FormMessagesMixin, DeleteView):
    model = Post
    form_valid_message = _('Your post has been deleted.')
    form_invalid_message = _('Error. Please, check your input and try again.')
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()

        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        location = self.request.GET.get('location')
        if location == 'base':
            response = HttpResponse()
            trigger_client_event(response, 'postDeleted')
        else:
            response = HttpResponseClientRedirect(reverse('forum:base-forum-page'))

        return response
