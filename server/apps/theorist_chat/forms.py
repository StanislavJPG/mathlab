from django import forms
from django.db import transaction
from django_bleach.forms import BleachField

from server.apps.theorist_chat.models import TheoristMessage, TheoristChatRoom


class TheoristMessageForm(forms.Form):
    message = BleachField(widget=forms.Textarea, max_length=500, required=True)

    @transaction.atomic
    def save(self, theorist, **kwargs):
        message = kwargs.get('message')
        room = TheoristChatRoom.objects.get(uuid=kwargs.get('room_uuid'))
        instance = TheoristMessage.objects.create(sender=theorist, message=message, room=room)
        return instance
