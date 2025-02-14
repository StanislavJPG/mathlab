from django import forms
from django.utils.translation import gettext_lazy as _

from server.apps.forum.models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "categories",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": _("Question topic (maximum 85 characters)")}
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": _("Describe your question here"),
                }
            ),
        }  # trans: Тема питання (не більше 85 символів)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        # prepare 'categories' field
        self.fields["categories"].label_from_instance = (
            lambda obj: obj.get_name_display()
        )
        self.instance.user = self.user
