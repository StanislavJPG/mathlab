from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_bleach.forms import BleachField
from tinymce.widgets import TinyMCE

from server.apps.theorist.models import Theorist
from server.apps.theorist_chat.models import TheoristMessage, TheoristChatRoom
from server.common.forms import ChoicesWithAvatarsWidget, MultipleChoicesWithAvatarsWidget


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
            settings__is_able_to_get_messages=True,
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


class ShareViaMessageForm(forms.Form):
    receiver = forms.ModelMultipleChoiceField(widget=MultipleChoicesWithAvatarsWidget, queryset=None)

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        self.i18n_obj_name = kwargs.pop('i18n_obj_name')
        self.instance_uuid = kwargs.pop('instance_uuid')
        self.sharing_instance = kwargs.pop('sharing_instance')
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

        self.fields['receiver'].queryset = Theorist.objects.filter(
            ~Q(uuid=self.theorist.uuid),
            (
                Q(chat_rooms_initiated__first_member=self.theorist)
                | Q(chat_rooms_received__second_member=self.theorist)
                | Q(chat_rooms_initiated__second_member=self.theorist)
                | Q(chat_rooms_received__first_member=self.theorist)
            ),
            settings__is_able_to_get_messages=True,
            chat_configuration__is_chats_available=True,
        ).distinct()
        self.room_qs = TheoristChatRoom.objects.filter(Q(first_member=self.theorist) | Q(second_member=self.theorist))
        self.fields['receiver'].label_from_instance = lambda obj: obj.full_name
        self.fields['receiver'].to_field_name = 'uuid'

    @mark_safe
    def _get_default_share_message(self, main_text_label=None, text_label=None):
        url_to_share = self.sharing_instance.get_share_url()
        main_text_label = _("I'm sharing with you!") if not main_text_label else main_text_label
        text_label = _('Hi! I`m sending you my %s. You are welcome by link below:') if not text_label else text_label

        return f"""
        <div class="d-flex justify-content-center align-items-center h-100">
          <div class="card shadow-lg rounded-4 p-4 text-center">
            <h2 class="mb-3">🌟 {main_text_label}</h2>
            <p class="lead">{text_label}</p>
            <a href="{url_to_share}" class="btn btn-primary mt-3">Check it out</a>
          </div>
        </div>
        """

    def save(self, *args):
        instances = self.cleaned_data['receiver']
        to_create = []
        for instance in instances:
            room = self.room_qs.get(Q(first_member=instance) | Q(second_member=instance))
            to_create.append(
                TheoristMessage(sender=self.theorist, room=room, message=self._get_default_share_message())
            )
        objs = TheoristMessage.objects.bulk_create(to_create)
        return objs
