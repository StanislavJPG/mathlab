import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.urls import reverse
from django.utils import dateformat, timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from server.apps.theorist_chat.forms import TheoristMessageForm
from server.apps.theorist_chat.models import TheoristMessage
from server.common.utils.helpers import limit_nbsp_paragraphs, is_valid_uuid


class TheoristChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_uuid = self.scope['url_route']['kwargs']['room_uuid']
        async_to_sync(self.channel_layer.group_add)(self.room_group_uuid, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_uuid, self.channel_name)

    @mark_safe
    def get_message_actions_as_html_tags(self, message_uuid):
        delete_msg_label = _('Delete')
        delete_confirmation_label = _(
            'Are you sure you want to delete this message? You can restore it in any time after doing that.'
        )
        reply_label = _('Reply')
        html_to_return = f"""
        <li>
          <button type="button"
                  data-toast-trigger
                  class="dropdown-item"
                  hx-get="{reverse('forum:theorist_chat:hx-messages-reply', args=[self.room_group_uuid, message_uuid])}"
                  onclick="document.querySelector('#chat-message-submit').setAttribute('data-reply-attr-uuid', '{message_uuid}')"
                  hx-target="#message-reply-block"
                  hx-trigger="click"
                  style="cursor: pointer">
            <i class="ti ti-message-reply"></i> {reply_label}
          </button>
        </li>
        <li>
          <hr class="dropdown-divider">
        </li>
        <li>
        <button class="dropdown-item text-danger"
                  data-toast-trigger
                  type="button"
                  hx-post="{reverse('forum:theorist_chat:chat-message-safe-delete', kwargs={'uuid': message_uuid})}"
                  hx-trigger="click"
                  hx-confirm="{delete_confirmation_label}"
                  style="cursor: pointer">
            <i class="ti ti-trash"></i> {delete_msg_label}
        </button>
        </li>
        """
        return html_to_return

    def _get_context(self):
        user = self.scope['user']
        response = {
            'theorist_avatar_url': user.theorist.get_current_avatar_url(),
            'theorist_uuid': str(user.theorist.uuid),
            'theorist_full_name': user.theorist.full_name,
            'theorist_profile_url': user.theorist.get_absolute_url(),
            'current_time': dateformat.format(timezone.localtime(timezone.now()), 'd E Y р. H:i'),
        }
        return response

    def save_data(self, **kwargs):
        msg = kwargs.get('message', '')
        msg_uuid_to_reply = kwargs.get('reply_message_uuid', '')
        user = self.scope['user']
        kwargs.update({'room_uuid': self.room_group_uuid})
        sanitized_form = TheoristMessageForm(msg_uuid_to_reply=msg_uuid_to_reply, data={'message': msg})
        if sanitized_form.is_valid():
            return sanitized_form.save(theorist=user.theorist, **kwargs)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        response = self._get_context()
        response['message'] = limit_nbsp_paragraphs(message)

        # Prepare message as reply message if it is
        response['reply_message_uuid'] = text_data_json['reply_message_uuid']
        msg_uuid_to_reply = text_data_json['reply_message_uuid']
        if msg_uuid_to_reply and is_valid_uuid(msg_uuid_to_reply[1:-1]):
            reply_msg = TheoristMessage.objects.filter(uuid=msg_uuid_to_reply[1:-1]).first()
            response['replied_to'] = {'sender_full_name': reply_msg.sender.full_name, 'message': reply_msg.message}

        message_obj = self.save_data(**response)

        theorist_html_actions = (
            self.get_message_actions_as_html_tags(message_obj.uuid) if hasattr(message_obj, 'uuid') else '<div></div>'
        )
        response.update(
            {
                'theorist_html_actions': theorist_html_actions,
                'room_uuid': self.room_group_uuid,
            }
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_uuid, {'type': 'chat_message', 'message': response}
        )

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event['message']))
