from django import forms
from django.utils.translation import gettext_lazy as _

from tinymce.widgets import TinyMCE

from server.apps.forum.models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "categories",
        )
        widgets = {
            "title": forms.TextInput(  # trans: Тема питання (не більше 85 символів)
                attrs={"placeholder": _("Question topic (maximum 85 characters)")}
            ),
            "content": TinyMCE(attrs={"cols": 30, "rows": 30}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        # prepare 'categories' field
        self.fields["categories"].label_from_instance = (
            lambda obj: obj.get_name_display()
        )
        self.instance.user = self.user


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
        widgets = {"comment": TinyMCE(attrs={"cols": 30, "rows": 30})}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.post = kwargs.pop("post")
        super().__init__(*args, **kwargs)
        self.instance.user = self.user
        self.instance.post = self.post
