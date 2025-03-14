from django import forms

from tinymce.widgets import TinyMCE

from server.apps.forum.models import Comment


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
