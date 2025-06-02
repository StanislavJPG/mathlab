from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from server.apps.forum.models.comment import CommentAnswer


class CommentAnswerCreateForm(forms.ModelForm):
    class Meta:
        model = CommentAnswer
        fields = ('text_body',)
        widgets = {'text_body': TinyMCE(attrs={'cols': 30, 'rows': 30, 'placeholder': _('Type your answer here')})}

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        self.comment = kwargs.pop('comment')
        super().__init__(*args, **kwargs)
        self.instance.theorist = self.theorist

    @transaction.atomic
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.comment.answers.add(instance)
        return instance
