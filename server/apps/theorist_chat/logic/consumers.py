import json

import uuid
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.urls import reverse
from django.utils import dateformat, timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from server.apps.theorist_chat.forms import TheoristMessageForm
from server.apps.theorist_chat.models import TheoristMessage, TheoristChatRoom
from server.common.utils.helpers import limit_nbsp_paragraphs, is_valid_uuid


class TheoristChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_uuid = self.scope['url_route']['kwargs']['room_uuid']
        async_to_sync(self.channel_layer.group_add)(self.room_group_uuid, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_uuid, self.channel_name)

    @mark_safe
    def get_message_actions_as_html_tags(self, message_uuid, as_receiver=False):
        reply_url = reverse('forum:theorist_chat:hx-messages-reply', args=[self.room_group_uuid, message_uuid])
        delete_url = reverse('forum:theorist_chat:chat-message-safe-delete', kwargs={'uuid': message_uuid})
        complain_url = reverse('complaints:complaint-create', args=('message', message_uuid))

        delete_msg_label = _('Delete')
        delete_confirmation_label = _(
            'Are you sure you want to delete this message? You can restore it in any time after doing that.'
        )
        reply_label = _('Reply')
        complain_label = _('Complain')

        reply_button = f"""
            <li>
                <button type="button"
                        data-toast-trigger
                        class="dropdown-item"
                        hx-get="{reply_url}"
                        hx-on:click="document.querySelector('#chat-message-submit').setAttribute('data-reply-attr-uuid', '{message_uuid}')"
                        hx-target="#message-reply-block"
                        hx-trigger="click"
                        style="cursor: pointer">
                    <i class="ti ti-message-reply"></i> {reply_label}
                </button>
            </li>
        """

        delete_button = f"""
            <li><hr class="dropdown-divider"></li>
            <li>
                <button class="dropdown-item text-danger"
                        data-toast-trigger
                        type="button"
                        hx-post="{delete_url}"
                        hx-trigger="click"
                        hx-confirm="{delete_confirmation_label}"
                        style="cursor: pointer">
                    <i class="ti ti-trash"></i> {delete_msg_label}
                </button>
            </li>
        """

        complain_button = ''
        if as_receiver:
            complain_button = f"""
                <li><hr class="dropdown-divider"></li>
                <li>
                    <button class="dropdown-item text-danger"
                            hx-get="{complain_url}"
                            hx-target="#complaint-modal"
                            data-bs-target="#complaint-modal"
                            data-bs-toggle="modal"
                            type="button">
                        <i class="ti ti-clipboard-x"></i> {complain_label}
                    </button>
                </li>
            """

        return reply_button + delete_button + complain_button

    def _get_context(self):
        user = self.scope['user']
        response = {
            'theorist_avatar_url': user.theorist.get_current_avatar(),
            'theorist_uuid': str(user.theorist.uuid),
            'theorist_full_name': user.theorist.full_name,
            'theorist_profile_url': user.theorist.get_absolute_url(),
            'current_time': dateformat.format(timezone.localtime(timezone.now()), 'd E Y р. H:i'),
        }
        return response

    def _get_ready_context(self, msg):
        theorist_html_actions = (
            self.get_message_actions_as_html_tags(msg.uuid) if hasattr(msg, 'uuid') else '<div></div>'
        )
        return {
            'theorist_html_actions': theorist_html_actions,
            'for_received_theorist_html_actions': self.get_message_actions_as_html_tags(msg.uuid, as_receiver=True)
            if hasattr(msg, 'uuid')
            else '<div></div>',
            'room_uuid': self.room_group_uuid,
        }

    def save_data(self, **kwargs):
        msg = kwargs.get('message', '')
        msg_uuid_to_reply = kwargs.get('reply_message_uuid', '')
        user = self.scope['user']
        kwargs.update({'room_uuid': self.room_group_uuid})
        sanitized_form = TheoristMessageForm(msg_uuid_to_reply=msg_uuid_to_reply, data={'message': msg})
        if sanitized_form.is_valid():
            return sanitized_form.save(theorist=user.theorist, **kwargs)

    def receive(self, text_data=None, bytes_data=None):
        response = self._get_context()

        if bytes_data:
            self.process_voice_message(bytes_data)
            return

        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            response['message'] = limit_nbsp_paragraphs(message)

            # Prepare message as reply message if it is
            response['reply_message_uuid'] = text_data_json['reply_message_uuid']
            msg_uuid_to_reply = text_data_json['reply_message_uuid']
            if msg_uuid_to_reply and is_valid_uuid(msg_uuid_to_reply):
                reply_msg = TheoristMessage.objects.filter(uuid=msg_uuid_to_reply).first()
                response['replied_to'] = {'sender_full_name': reply_msg.sender.full_name, 'message': reply_msg.message}

            message_obj = self.save_data(**response)
            response.update(self._get_ready_context(message_obj))

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_uuid, {'type': 'chat_message', 'message': response}
            )

    def process_voice_message(self, bytes_data):
        filename = f'{uuid.uuid4()}.wav'
        user = self.scope['user']

        room = TheoristChatRoom.objects.get(uuid=self.room_group_uuid)
        msg = TheoristMessage.objects.create(
            audio_message=ContentFile(bytes_data, name=filename), room=room, sender=user.theorist
        )
        context = self._get_context()
        context.update(self._get_ready_context(msg))
        context.update(
            {
                'is_voice': True,
                'voice_html_block': f"""
                <div class="card-body voice-gap voice-gap-{str(msg.uuid)}">
                  <audio crossorigin>
                    <source src="{msg.audio_message.url}" type="audio/wav">
                  </audio>
                </div>
                """,
                'msg_uuid': str(msg.uuid),
            }
        )

        async_to_sync(self.channel_layer.group_send)(self.room_group_uuid, {'type': 'chat_message', 'message': context})

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event['message']))
