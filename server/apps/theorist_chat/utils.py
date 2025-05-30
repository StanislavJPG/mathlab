"""Utility functions related to the theorist_chat app."""

from django.db.models import Q

from server.apps.theorist_chat.constants import DEFAULT_MAILBOX_PAGINATION
from server.apps.theorist_chat.models import TheoristChatRoom
from server.common.utils.paginator import page_resolver


def get_mailbox_url(*, target_room, some_member, chat_room_qs=None, paginate_by=DEFAULT_MAILBOX_PAGINATION):
    """Function that takes target_room and theorist as required args
    and returns completed mailbox URL with a stunning UX on frontend"""
    if some_member and not chat_room_qs:
        chat_room_qs = TheoristChatRoom.objects.filter(
            Q(first_member=some_member) | Q(second_member=some_member)
        ).order_by_last_sms_sent_relevancy()

    page_for_url = page_resolver.get_page_for_paginated_qs(
        qs=chat_room_qs,
        target_obj=target_room,
        paginate_by=paginate_by,
    )
    return target_room.get_absolute_url(next_uuid=target_room.uuid, mailbox_page=page_for_url)
