from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_bleach.forms import BleachField
from tinymce.widgets import TinyMCE

from server.apps.theorist.models import Theorist
from server.apps.theorist_chat.models import TheoristMessage, TheoristChatRoom
from server.common.forms import ChoicesWithAvatarsWidget


class TheoristMessageForm(forms.Form):
    message = BleachField(widget=forms.Textarea, max_length=500, required=True)

    @transaction.atomic
    def save(self, theorist, **kwargs):
        message = kwargs.get('message')
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


class ShareViaMessageForm(forms.ModelForm):
    class Meta:
        model = TheoristMessage
        fields = ('room',)

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        self.kwarg_instance = kwargs.pop('kwarg_instance')
        self.i18n_obj_name = kwargs.pop('i18n_obj_name')
        self.model_instance_label = kwargs.pop('model_instance_label')
        self.instance_uuid = kwargs.pop('instance_uuid')
        super().__init__(*args, **kwargs)
        self.instance.sender = self.theorist
        self.instance.message = self._get_default_share_message()

    @mark_safe
    def _get_default_share_message(self):
        model = self.model_instance_label
        url_to_share = model.get_share_url(uuid=self.instance_uuid)
        return f'Here is your url {url_to_share}'  # todo: Change

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save(commit=True)
