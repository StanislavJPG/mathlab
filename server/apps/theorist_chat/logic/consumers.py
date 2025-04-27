import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import dateformat
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from server.apps.theorist_chat.forms import TheoristMessageForm
from server.common.utils.helpers import limit_nbsp_paragraphs


class TheoristChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_uuid = self.scope['url_route']['kwargs']['room_uuid']
        async_to_sync(self.channel_layer.group_add)(self.room_group_uuid, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_uuid, self.channel_name)

    @mark_safe
    def get_message_actions_as_html_tags(self):
        user = self.scope['user']  # todo: change # noqa: F841
        delete_msg_label = _('Delete message for all members')
        confirmation_label = _(
            'Are you sure you want to delete this message? You can restore it in any time after doing that.'
        )
        html_to_return = f"""
        <li>
        <button class="dropdown-item text-danger"
                  type="button"
                  hx-get=""
                  hx-trigger="click"
                  hx-target=""
                  hx-confirm="{confirmation_label}"
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
            'theorist_html_actions': self.get_message_actions_as_html_tags(),
            'theorist_full_name': user.theorist.full_name,
            'theorist_profile_url': user.theorist.get_absolute_url(),
            'theorist_created_at': dateformat.format(user.theorist.created_at, 'd E Y р. H:i'),
        }
        return response

    def _save_data_to_db(self, **kwargs):
        msg = kwargs.get('message', '')
        user = self.scope['user']
        kwargs.update({'room_uuid': self.room_group_uuid})
        sanitized_form = TheoristMessageForm(data={'message': msg})
        if sanitized_form.is_valid():
            sanitized_form.save(theorist=user.theorist, **kwargs)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        response = self._get_context()
        response.update({'message': limit_nbsp_paragraphs(message)})
        self._save_data_to_db(**response)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_uuid, {'type': 'chat_message', 'message': response}
        )

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event['message']))
