from django import forms
from django.db import transaction
from django.db.models import Q
from django_bleach.forms import BleachField

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
            ~Q(uuid=self.first_member.uuid),
            chat_group__is_chats_available=True,  # todo: fix
        )
        self.fields['second_member'].label_from_instance = lambda obj: obj.full_name
        self.fields['second_member'].to_field_name = 'uuid'
