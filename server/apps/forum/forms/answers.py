from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from server.apps.forum.models.comment import CommentAnswer
from server.apps.theorist_notifications.signals import notify


class CommentAnswerCreateForm(forms.ModelForm):
    send_to_post_owner = forms.BooleanField(required=False)

    class Meta:
        model = CommentAnswer
        fields = ('text_body', 'send_to_post_owner')
        widgets = {
            'text_body': TinyMCE(
                attrs={'cols': 30, 'rows': 30, 'placeholder': _('Type your answer here')},
                mce_attrs={
                    'toolbar': 'undo redo | formatselect | eqneditor',
                },
            )
        }

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        self.comment = kwargs.pop('comment')
        super().__init__(*args, **kwargs)
        self.instance.theorist = self.theorist

    def clean(self):
        cleaned_data = super().clean()
        if not self.comment.is_able_to_get_answers:
            self.add_error(None, _('You are not able to add answer to this comment.'))
        return cleaned_data

    def _process_notifications(self, *, instance):
        display_name_label = _('has answered to comment, which you are following')
        recipients = (
            instance.theorist.user
            if not self.cleaned_data.get('send_to_post_owner')
            else [instance.theorist.user, instance.post.theorist.user]
        )
        notify.send(
            sender=self.theorist,
            recipient=recipients,
            actor_content_type=ContentType.objects.get_for_model(instance.theorist),
            target=instance,
            action_object=instance,
            public=False,
            action_url=instance.get_absolute_url(),
            target_display_name=display_name_label,
        )

    @transaction.atomic
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.comment.answers.add(instance)
            self._process_notifications(instance=self.comment)
        return instance
