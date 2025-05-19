from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from honeypot.decorators import check_honeypot

from server.apps.forum.models import Comment, Post
from server.apps.theorist_chat.forms import ShareViaMessageForm
from server.apps.theorist_drafts.models import TheoristDraftsConfiguration
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin, CaptchaViewMixin


@method_decorator(check_honeypot, name='post')
class AbstractMessageInstanceShareView(
    LoginRequiredMixin, HXViewMixin, FormMessagesMixin, CaptchaViewMixin, CreateView
):
    template_name = 'modals/messages_share_instance.html'
    form_class = ShareViaMessageForm
    success_url = None

    def get_i18n_instance_name(self):
        raise NotImplementedError('Specify `get_i18n_instance_name` method')

    def get_instance_to_share(self):
        # Actually, this method returns instance that we try to share with other theorists.
        raise NotImplementedError('Specify `get_instance_to_share` method')

    def get_qs_to_filter(self):
        # This method returns queryset of instance specific objects.
        raise NotImplementedError('Specify `get_qs_to_filter` method')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['i18n_obj_name'] = self.get_i18n_instance_name()
        return context

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        kwargs['theorist'] = self.request.theorist
        kwargs['instance_uuid'] = self.kwargs['instance_uuid']
        kwargs['sharing_instance'] = self.get_instance_to_share()
        kwargs['qs_to_filter'] = self.get_qs_to_filter()
        kwargs['i18n_obj_name'] = self.get_i18n_instance_name()
        return kwargs

    def get_form_valid_message(self):
        i18n_instance = self.get_i18n_instance_name()
        return force_str(_('You successfully shared %s.') % i18n_instance)

    def get_form_invalid_message(self):
        i18n_instance = self.get_i18n_instance_name()
        return force_str(_('Error while sharing %s. Please check for errors and try again.') % i18n_instance)

    def form_valid(self, form):
        self.captcha_process(form)
        form.save()
        self.messages.success(self.get_form_valid_message(), fail_silently=True)
        return HttpResponse(status=201)


class MessageDraftShareView(AbstractMessageInstanceShareView):
    success_url = reverse_lazy('mathlab:drafts:base-drafts')

    def get_instance_to_share(self):
        return TheoristDraftsConfiguration.objects.filter_by_is_public_available().get(
            uuid=self.kwargs['instance_uuid']
        )

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        kwargs['url_to_share'] = self.get_instance_to_share().get_share_url()
        return kwargs

    def get_qs_to_filter(self):
        instance = self.get_instance_to_share()
        return instance.theorist.drafts.all()

    def get_i18n_instance_name(self):
        return _('drafts')


class MessageCommentShareView(AbstractMessageInstanceShareView):
    def get_instance_to_share(self):
        return Comment.objects.get(uuid=self.kwargs['instance_uuid'])

    def get_qs_to_filter(self):
        return Comment.objects.filter(uuid=self.kwargs['instance_uuid'])

    def get_i18n_instance_name(self):
        return _('comment')

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        instance = self.get_instance_to_share()
        kwargs['url_to_share'] = instance.get_absolute_url(self.request.GET.get('page'))
        return kwargs

    def get_success_url(self):
        instance = self.get_instance_to_share().post
        return reverse_lazy('forum:post-details', kwargs={'pk': instance.pk, 'slug': instance.slug})


class MessagePostShareView(AbstractMessageInstanceShareView):
    def get_instance_to_share(self):
        return Post.objects.get(uuid=self.kwargs['instance_uuid'])

    def get_qs_to_filter(self):
        return Post.objects.filter(uuid=self.kwargs['instance_uuid'])

    def get_i18n_instance_name(self):
        return _('post')

    def get_form_kwargs(self):
        self.request: AuthenticatedHttpRequest
        kwargs = super().get_form_kwargs()
        instance = self.get_instance_to_share()
        kwargs['url_to_share'] = instance.get_absolute_url()
        return kwargs

    def get_success_url(self):
        instance = self.get_instance_to_share()
        return reverse_lazy('forum:post-details', kwargs={'pk': instance.pk, 'slug': instance.slug})
