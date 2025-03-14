from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from server.apps.forum.models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'categories',
        )
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Question topic (maximum 85 characters)')}),
            'content': TinyMCE(attrs={'cols': 30, 'rows': 30}),
        }

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        super().__init__(*args, **kwargs)
        # prepare 'categories' field
        self.fields['categories'].label_from_instance = lambda obj: obj.get_name_display()
        self.instance.theorist = self.theorist

    def clean_categories(self):
        categories = self.cleaned_data['categories']
        if len(categories) > 4:
            self.add_error(
                'categories',
                _('You cannot choose more then %s categories.') % Post.CATEGORIES_LIMIT,
            )
        return categories


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
        widgets = {'content': TinyMCE(attrs={'cols': 30, 'rows': 30})}
