import base64
import json
import uuid
from io import BytesIO

from asgiref.sync import async_to_sync
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone, dateformat
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from channels.generic.websocket import WebsocketConsumer

from server.apps.theorist_chat.forms import TheoristMessageForm
from server.apps.theorist_chat.models import TheoristMessage
from server.common.utils.helpers import is_valid_uuid, limit_nbsp_paragraphs


class TheoristChatConsumer(WebsocketConsumer):
    def connect(self) -> None:
        self.room_group_uuid = self.scope['url_route']['kwargs']['room_uuid']
        async_to_sync(self.channel_layer.group_add)(self.room_group_uuid, self.channel_name)
        self.accept()

    def disconnect(self, close_code: int) -> None:
        async_to_sync(self.channel_layer.group_discard)(self.room_group_uuid, self.channel_name)

    def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        """
        Main entry point for incoming websocket messages.
        """
        if not text_data:
            return

        payload = json.loads(text_data)
        # Voice message handling
        if payload.get('is_voice', False):
            self._handle_voice_message(payload)
            return

        # Text message handling
        message = payload.get('message', '')
        reply_uuid = payload.get('reply_message_uuid', '')

        context = self._get_base_context()
        context['message'] = limit_nbsp_paragraphs(message)
        context['reply_message_uuid'] = reply_uuid
        context = self._process_reply(reply_uuid, context)

        message_obj = self._save_message(context)
        context.update(self._get_message_context(message_obj))

        # Add voice HTML block if replying to a voice message
        if context.get('replied_to', {}).get('is_voice', False):
            context['replied_to']['voice_html_block'] = self._get_voice_message_html(message_obj, is_replied=True)

        async_to_sync(self.channel_layer.group_send)(self.room_group_uuid, {'type': 'chat_message', 'message': context})

    def chat_message(self, event: dict) -> None:
        """
        Handler for messages sent to the channel group.
        Sends data back to WebSocket client.
        """
        self.send(text_data=json.dumps(event['message']))

    def _handle_voice_message(self, payload: dict) -> None:
        """
        Process incoming voice message payload.
        """
        audio_b64 = payload['audio_base64']
        audio_bytes = base64.b64decode(audio_b64)
        filename = f'{uuid.uuid4()}.wav'

        content_file = ContentFile(audio_bytes, name=filename)
        uploaded_audio = InMemoryUploadedFile(
            file=BytesIO(content_file.read()),
            field_name='audio_message',
            name=filename,
            content_type='audio/wav',
            size=len(audio_bytes),
            charset=None,
        )

        reply_uuid = payload.get('reply_message_uuid')
        context = self._get_base_context()
        context = self._process_reply(reply_uuid, context)
        context['reply_message_uuid'] = reply_uuid
        context['audio_message'] = uploaded_audio

        message_obj = self._save_message(context)
        context.pop('audio_message', None)
        context.update(self._get_message_context(message_obj))

        context.update(
            {
                'is_voice': True,
                'voice_html_block': self._get_voice_message_html(message_obj),
            }
        )

        if context.get('replied_to', {}).get('is_voice', False):
            context['replied_to']['voice_html_block'] = self._get_voice_message_html(message_obj, is_replied=True)

        async_to_sync(self.channel_layer.group_send)(self.room_group_uuid, {'type': 'chat_message', 'message': context})

    def _get_base_context(self) -> dict:
        """
        Base context info common to all messages.
        """
        user = self.scope['user']
        return {
            'theorist_avatar_url': user.theorist.get_current_avatar(),
            'theorist_uuid': str(user.theorist.uuid),
            'theorist_full_name': user.theorist.full_name,
            'theorist_profile_url': user.theorist.get_absolute_url(),
            'current_time': dateformat.format(timezone.localtime(timezone.now()), 'd E Y р. H:i'),
        }

    def _process_reply(self, reply_uuid: str | None, context: dict) -> dict:
        """
        If the message is a reply, attach info about the replied message.
        """
        if reply_uuid and is_valid_uuid(reply_uuid):
            reply_msg = TheoristMessage.objects.filter(uuid=reply_uuid).first()
            if reply_msg:
                context['replied_to'] = {
                    'sender_full_name': reply_msg.sender.full_name,
                    'message': reply_msg.message,
                    'is_voice': bool(reply_msg.audio_message.name),
                }
        return context

    def _save_message(self, context: dict) -> TheoristMessage | None:
        """
        Saves the message form with text/audio and returns the created message object.
        """
        msg = context.get('message', '')
        audio_msg = context.get('audio_message', None)
        reply_uuid = context.get('reply_message_uuid', '')

        user = self.scope['user']
        data = {'message': msg}
        files = {'audio_message': audio_msg} if audio_msg else None

        form = TheoristMessageForm(msg_uuid_to_reply=reply_uuid, data=data, files=files or None)
        if form.is_valid():
            return form.save(theorist=user.theorist, room_uuid=self.room_group_uuid)
        return None

    def _get_message_context(self, msg: TheoristMessage | None) -> dict:
        """
        Return message-specific context for frontend consumption.
        """
        if not msg or not hasattr(msg, 'uuid'):
            return {
                'theorist_html_actions': '<div></div>',
                'for_received_theorist_html_actions': '<div></div>',
                'room_uuid': self.room_group_uuid,
                'msg_uuid': None,
            }

        return {
            'theorist_html_actions': self._get_message_actions_html(msg.uuid),
            'for_received_theorist_html_actions': self._get_message_actions_html(msg.uuid, as_receiver=True),
            'room_uuid': self.room_group_uuid,
            'msg_uuid': str(msg.uuid),
        }

    @mark_safe
    def _get_message_actions_html(self, message_uuid: str, as_receiver: bool = False) -> str:
        """
        Generate HTML for message action buttons (Reply, Delete, Complain).
        """
        reply_url = reverse('forum:theorist_chat:hx-messages-reply', args=[self.room_group_uuid, message_uuid])
        delete_url = reverse('forum:theorist_chat:chat-message-safe-delete', kwargs={'uuid': message_uuid})
        complain_url = reverse('complaints:complaint-create', args=('message', message_uuid))

        delete_label = _('Delete')
        delete_confirm = _('Are you sure you want to delete this message? You can restore it anytime after doing that.')
        reply_label = _('Reply')
        complain_label = _('Complain')

        reply_btn = f"""
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

        delete_btn = f"""
            <li><hr class="dropdown-divider"></li>
            <li>
                <button class="dropdown-item text-danger"
                        data-toast-trigger
                        type="button"
                        hx-post="{delete_url}"
                        hx-trigger="click"
                        hx-confirm="{delete_confirm}"
                        style="cursor: pointer">
                    <i class="ti ti-trash"></i> {delete_label}
                </button>
            </li>
        """

        complain_btn = ''
        if as_receiver:
            complain_btn = f"""
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

        return reply_btn + delete_btn + complain_btn

    def _get_voice_message_html(self, msg: TheoristMessage, is_replied: bool = False) -> str:
        """
        Generate HTML block for voice message audio player.
        """
        uuid_str = str(msg.uuid)
        url = msg.replied_to.audio_message.url if is_replied else msg.audio_message.url

        css_class = f'voice-ws-reply-gap-{uuid_str}' if is_replied else f'voice-gap-{uuid_str}'

        return f"""
            <div class="card-body voice-gap {css_class}" data-voice-uuid="{uuid_str}">
                <audio crossorigin>
                    <source src="{url}" type="audio/wav">
                </audio>
            </div>
        """
