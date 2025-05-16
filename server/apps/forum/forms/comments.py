from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from tinymce.widgets import TinyMCE

from server.apps.forum.models import Comment
from server.apps.theorist_notifications.signals import notify


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {'comment': TinyMCE(attrs={'cols': 30, 'rows': 30})}

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        self.post = kwargs.pop('post')
        super().__init__(*args, **kwargs)
        self.instance.theorist = self.theorist
        self.instance.post = self.post

    def save(self, commit=True):
        instance = super().save(commit=commit)
        display_name_label = _('has commented post %s, that you are following') % instance.post.title
        notify.send(
            sender=self.theorist,
            recipient=instance.post.theorist.user,
            actor_content_type=ContentType.objects.get_for_model(instance.post.theorist),
            target=instance,
            action_object=instance,
            public=False,
            verb='',
            action_url=instance.get_absolute_url(),
            target_display_name=display_name_label,
        )
        return instance


class CommentUpdateForm(forms.ModelForm):
    predefined_comment = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 30}))

    class Meta:
        model = Comment
        # change field name only for skip form conflicts
        fields = ('predefined_comment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['predefined_comment'].initial = self.instance.comment

    def save(self, commit=True):
        self.instance.comment = self.cleaned_data['predefined_comment']
        self.instance.save(update_fields=['comment'])
