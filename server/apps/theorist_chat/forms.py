from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_bleach.forms import BleachField
from tinymce.widgets import TinyMCE

from server.apps.theorist.models import Theorist
from server.apps.theorist_chat.models import TheoristMessage, TheoristChatRoom
from server.common.forms import ChoicesWithAvatarsWidget, MultipleChoicesWithAvatarsWidget, CaptchaForm
from server.common.utils.helpers import limit_nbsp_paragraphs


class TheoristMessageForm(forms.Form):
    message = BleachField(widget=forms.Textarea, max_length=500, min_length=1, required=True)

    def clean_message(self):
        message = self.cleaned_data['message']
        return limit_nbsp_paragraphs(message)

    def validate_room(self, room) -> bool:
        first_member = room.first_member
        second_member = room.second_member
        first_cond = first_member.blacklist.blocked_theorists.filter(id=second_member.id).exists()
        second_cond = second_member.blacklist.blocked_theorists.filter(id=first_member.id).exists()
        if first_cond or second_cond:
            raise forms.ValidationError(_('Error. This theorist has blocked you.'))
        return True

    @transaction.atomic
    def save(self, theorist, **kwargs):
        message = self.cleaned_data['message']
        room = TheoristChatRoom.objects.get(uuid=kwargs.get('room_uuid'))
        if self.validate_room(room) is True:
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

        qs_to_exclude = (
            Theorist.objects.filter(
                (
                    Q(chat_rooms_initiated__first_member=self.first_member)
                    | Q(chat_rooms_received__second_member=self.first_member)
                )
                | (
                    Q(chat_rooms_received__first_member=self.first_member)
                    | Q(chat_rooms_initiated__second_member=self.first_member)
                )
            )
            .values_list('id', flat=True)
            .distinct()
        )
        self.fields['second_member'].queryset = (
            Theorist.objects.filter(~Q(uuid=self.first_member.uuid))
            .exclude(id__in=qs_to_exclude)
            .filter_is_chats_available()
            .filter_is_able_to_get_messages()
            .filter_by_accepted_friendship_as_member(member=self.first_member)
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


class ShareViaMessageForm(CaptchaForm, forms.Form):
    receiver = forms.ModelMultipleChoiceField(widget=MultipleChoicesWithAvatarsWidget, queryset=None)

    def __init__(self, *args, **kwargs):
        self.theorist = kwargs.pop('theorist')
        self.request = kwargs.pop('request')
        self.i18n_obj_name = kwargs.pop('i18n_obj_name')
        self.instance_uuid = kwargs.pop('instance_uuid')
        self.qs_to_filter = kwargs.pop('qs_to_filter')
        self.sharing_instance = kwargs.pop('sharing_instance')
        self.url_to_share = kwargs.pop('url_to_share')
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

        if self.qs_to_filter.exists():
            self.fields['receiver'].queryset = (
                Theorist.objects.filter(~Q(uuid=self.theorist.uuid))
                .filter_by_accepted_friendship_as_member(member=self.theorist)
                .filter_is_able_to_get_messages()
                .filter_is_chats_available()
                .distinct()
            )
        else:
            self.fields['receiver'].queryset = Theorist.objects.none()
            self.fields['receiver'].disabled = True
            self.fields['receiver'].help_text = (
                '* ' + _('You need to have any %s to share it with others.') % self.i18n_obj_name
            )

        self.fields['receiver'].label_from_instance = lambda obj: obj.full_name
        self.fields['receiver'].to_field_name = 'uuid'

    @mark_safe
    def _get_default_share_message(self, main_text_label=None, text_label=None):
        main_text_label = _("I'm sharing with you!") if not main_text_label else main_text_label
        text_label = (
            _("Hi! I'm sending <strong>%s</strong> to you. You can check it out by the link below:")
            % self.i18n_obj_name
            if not text_label
            else text_label
        )

        return f"""
        <div class="d-flex justify-content-center align-items-center h-100">
          <div class="card shadow-lg rounded-4 p-4 text-center">
            <h2 class="mb-3">🌟 {main_text_label}</h2>
            <p class="lead">{text_label}</p>
            <a href="{self.url_to_share}" class="btn btn-primary mt-3">Check it out</a>
          </div>
        </div>
        """

    @transaction.atomic
    def save(self):
        instances = self.cleaned_data['receiver']
        to_create = []
        for instance in instances:
            room, _ = TheoristChatRoom.objects.filter(
                (Q(first_member=self.theorist) & Q(second_member=instance))
                | (Q(first_member=instance) & Q(second_member=self.theorist)),
            ).get_or_create(first_member=self.theorist, second_member=instance)
            msg_obj = TheoristMessage(sender=self.theorist, room=room, message=self._get_default_share_message())
            to_create.append(msg_obj)

            # The model’s save() method will not be called, and the pre_save and post_save signals will not be sent:
            # https://docs.djangoproject.com/en/5.1/ref/models/querysets/#bulk-create
            msg_obj.before_create()

        objs = TheoristMessage.objects.bulk_create(to_create)
        return objs
