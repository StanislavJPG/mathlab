from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django_bleach.forms import BleachField
from tinymce.widgets import TinyMCE

from server.apps.theorist.models import Theorist
from server.apps.theorist_chat.models import TheoristMessage, TheoristChatRoom
from server.common.forms import ChoicesWithAvatarsWidget
from server.common.utils.helpers import limit_nbsp_paragraphs


class TheoristMessageForm(forms.Form):
    message = BleachField(widget=forms.Textarea, max_length=500, min_length=1, required=True)

    def clean_message(self):
        message = self.cleaned_data['message']
        return limit_nbsp_paragraphs(message)

    @transaction.atomic
    def save(self, theorist, **kwargs):
        message = self.cleaned_data['message']
        room = TheoristChatRoom.objects.get(uuid=kwargs.get('room_uuid'))
        instance = TheoristMessage.objects.create(sender=theorist, message=message, room=room)
        return instance


class MailBoxCreateForm(forms.ModelForm):
    second_member = forms.ModelChoiceField(queryset=None, widget=ChoicesWithAvatarsWidget, required=True)

    class Meta:
        model = TheoristChatRoom
        fields = ('second_member',)

    def __init__(self, *args, **kwargs):
        self.first_member = kwargs.pop('theorist')
        super().__init__(*args, **kwargs)
        self.instance.first_member = self.first_member

        self.fields['second_member'].queryset = Theorist.objects.filter(
            (
                ~Q(uuid=self.first_member.uuid) & Q(chat_configuration__is_chats_available=True)
            ),  # TODO: Set only for friends
            (Q(settings__is_able_to_get_messages=True) | Q(settings__is_able_to_get_messages=True)),
        )
        self.fields['second_member'].label_from_instance = lambda obj: obj.full_name
        self.fields['second_member'].to_field_name = 'uuid'

    def clean_second_member(self):
        second_member = self.cleaned_data['second_member']
        is_room_exists = TheoristChatRoom.objects.filter(
            (Q(first_member=self.first_member) & Q(second_member=second_member))
            | (Q(first_member=second_member) & Q(second_member=self.first_member)),
        ).exists()
        if is_room_exists:
            self.add_error('second_member', _('This mailbox is already exists.'))
        return second_member


class MessageMessageSingleForm(forms.Form):
    # this form exists because of this https://github.com/django-blog-zinnia/zinnia-wysiwyg-tinymce/issues/6
    message = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 30}), max_length=500, required=True)
