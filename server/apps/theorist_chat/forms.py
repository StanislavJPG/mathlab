from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_bleach.forms import BleachField
from tinymce.widgets import TinyMCE

from server.apps.theorist.models import Theorist
from server.apps.theorist_chat.utils import get_mailbox_url
from server.apps.theorist_chat.models import TheoristMessage, TheoristChatRoom
from server.apps.theorist_drafts.models import TheoristDrafts
from server.apps.theorist_notifications.models import TheoristNotification
from server.apps.theorist_notifications.signals import notify
from server.common.forms import ChoicesWithAvatarsWidget, MultipleChoicesWithAvatarsWidget, CaptchaForm
from server.common.mixins.forms import TinyMCEMediaFormMixin
from server.common.utils.helpers import limit_nbsp_paragraphs, is_valid_uuid


class TheoristMessageForm(forms.Form):
    message = BleachField(widget=forms.Textarea, max_length=500, min_length=1, required=True)

    def __init__(self, *args, **kwargs):
        self.msg_uuid_to_reply = kwargs.pop('msg_uuid_to_reply')
        super().__init__(*args, **kwargs)
        msg_uuid_to_reply = self.msg_uuid_to_reply
        if msg_uuid_to_reply and is_valid_uuid(msg_uuid_to_reply):
            self.message_to_reply = (
                TheoristMessage.objects.filter(uuid=msg_uuid_to_reply).filter_by_is_not_safe_deleted().first()
            )
        else:
            self.message_to_reply = None

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

    def _process_notifications(self, *, theorist, message, room):
        display_name_label = _('has wrote you a message')
        recipient = room.first_member if room.first_member != theorist else room.second_member
        notify.send(
            sender=theorist,
            recipient=recipient.user,
            actor_content_type=ContentType.objects.get_for_model(recipient),
            target=message,
            action_object=message,
            public=False,
            action_url=get_mailbox_url(target_room=message.room, some_member=theorist),
            target_display_name=display_name_label,
        )

        # next we are clearing all unread messages for sender in current chat
        message_ids = list(map(str, room.messages.values_list('id', flat=True)))
        TheoristNotification.objects.filter(
            target_object_id__in=message_ids,
            theorist=theorist,
        ).unread().mark_all_as_read()

    @transaction.atomic
    def save(self, theorist, **kwargs):
        message = self.cleaned_data['message']
        room = TheoristChatRoom.objects.get(uuid=kwargs.get('room_uuid'))
        if self.validate_room(room) is True:
            instance = TheoristMessage.objects.create(
                sender=theorist, message=message, room=room, replied_to=self.message_to_reply
            )
            self._process_notifications(theorist=theorist, message=instance, room=room)
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
            .distinct()
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


class MessageMessageSingleForm(TinyMCEMediaFormMixin, forms.Form):
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
        self.is_rate_limited = kwargs.pop('is_rate_limited')
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

    def clean(self):
        cleaned_data = super().clean()
        if self.is_rate_limited:
            self.add_error(None, _('🏁 Slow down! Too many requests! Wait a while...'))
        return cleaned_data

    @mark_safe
    def _get_default_share_message(self, main_text_label=None, text_label=None, button_label=None):
        main_text_label = _("I'm sharing with you!") if not main_text_label else main_text_label
        text_label = (
            _("Hi! I'm sending <strong>%s</strong> to you. You can check it out by the link below:")
            % self.i18n_obj_name
            if not text_label
            else text_label
        )
        button_label = button_label if button_label else _('Check it out')

        return f"""
        <div class="d-flex justify-content-center align-items-center h-100">
          <div class="card shadow-lg rounded-4 p-4 text-center">
            <h2 class="mb-3">🌟 {main_text_label}</h2>
            <p class="lead">{text_label}</p>
            <a href="{self.url_to_share}" class="btn btn-primary mt-3"><i class="ti ti-corner-up-right"></i> {button_label}</a>
          </div>
        </div>
        """

    def _process_notifications(self, instance, ver_label=None):
        verb_label = _('has shared with you with') if not ver_label else ver_label
        return notify.send(
            sender=self.theorist,
            recipient=instance.user,
            actor_content_type=ContentType.objects.get_for_model(instance),
            target=self.sharing_instance,
            action_object=self.sharing_instance,
            public=False,
            verb=verb_label,
            action_url=self.url_to_share,
            target_display_name=self.i18n_obj_name,
        )

    @transaction.atomic
    def save(self):
        instances = self.cleaned_data['receiver']
        to_create = []
        for instance in instances:
            room = TheoristChatRoom.get_room(self.theorist, instance)
            if not room:
                room = TheoristChatRoom.objects.create(first_member=self.theorist, second_member=instance)

            msg_obj = TheoristMessage(
                sender=self.theorist, room=room, message=self._get_default_share_message(), is_system=True
            )
            to_create.append(msg_obj)

            # The model’s save() method will not be called, and the pre_save and post_save signals will not be sent:
            # https://docs.djangoproject.com/en/5.1/ref/models/querysets/#bulk-create
            msg_obj.before_create()
            self._process_notifications(instance)

        objs = TheoristMessage.objects.bulk_create(to_create)
        return objs


class DraftsShareViaMessageForm(ShareViaMessageForm):
    def __init__(self, *args, **kwargs):
        self.drafts_to_share: list = [uuid for uuid in kwargs.pop('drafts_to_share', []) if is_valid_uuid(uuid)]
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.drafts_to_share or len(self.drafts_to_share) > 10:
            self.add_error(None, _('You are not able to choose so many drafts to share.'))
        return cleaned_data

    def _process_notifications(self, instance, ver_label=None):
        verb_label = _('has shared with you with') if not ver_label else ver_label
        room = TheoristChatRoom.get_room(self.theorist, instance)
        return notify.send(
            sender=self.theorist,
            recipient=instance.user,
            actor_content_type=ContentType.objects.get_for_model(instance),
            target=self.sharing_instance,
            action_object=self.sharing_instance,
            public=False,
            verb=verb_label,
            action_url=get_mailbox_url(target_room=room, some_member=instance),
            target_display_name=self.i18n_obj_name,
        )

    @mark_safe
    def _get_default_share_message(self):
        pics = TheoristDrafts.objects.filter(uuid__in=self.drafts_to_share)

        if pics.count() <= 2:
            img_style = 'min-width: 220px;'
        else:
            img_style = 'min-width: 200px;'

        pics_owner = getattr(pics.first(), 'theorist')
        if pics_owner.uuid == self.theorist.uuid:
            main_text_label = _('I share my drafts with you!')
            url_to_share = self.url_to_share
        else:
            main_text_label = _("I share %s's drafts with you!") % pics_owner.full_name
            url_to_share = pics_owner.drafts_configuration.get_share_url()
        btn_label = _('See all available drafts')

        return f"""
        <div class="d-flex justify-content-center align-items-center h-100">
          <div class="card shadow-lg rounded-4 p-4 text-center" style="max-width: 700px; width: 100%;">
            <h5 class="mb-3">📝 {main_text_label}</h5>
            <div class="mb-3 row row-cols-1 g-3 row-cols-lg-3 justify-content-center d-flex align-items-center" id="gallery">
              {
            ''.join(
                f'''
                    <div class="col d-flex flex-column align-items-center me-2">
                        <a href="{pic.get_draft().url}"
                           data-pswp-width="{pic.get_draft().width}"
                           data-pswp-height="{pic.get_draft().height}"
                           target="_blank">
                          <img src="{pic.get_draft().url}" 
                               class="img-thumbnail rounded border border-2 shadow-sm mb-1" 
                               style="{img_style}" 
                               alt="preview">
                        </a>
                        <span class="small text-muted text-center" style="max-width: 200px; word-break: break-word;">
                            {pic.label}
                        </span>
                    </div>
                    '''
                for pic in pics
            )
        }
            </div>
            <a href="{url_to_share}" class="btn btn-primary mt-3"><i class="ti ti-corner-up-right"></i> {btn_label}</a>
          </div>
        </div>
        """
