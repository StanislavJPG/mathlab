from django.core.cache import cache
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from chat.models import Message
from chat.serializer import MessageSerializer
from forum.utils import PaginationCreator, delete_keys_matching_pattern
from users.serializers import ProfileSerializer


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, receiver: int, username: str):
        page = request.GET.get('page')
        cached_data = cache.get(f'receiver_id.{receiver}: '
                                f'receiver_name.{username}.'
                                f'page.{page}')
        pagination = PaginationCreator(page, limit=8)
        offset = pagination.get_offset

        if not cached_data:
            messages = Message.objects.filter(sender__in=[request.user.id, receiver],
                                              receiver__in=[request.user.id, receiver]
                                              ).order_by('-sent_at')[offset:offset+8]

            msg_serializer = MessageSerializer(messages, many=True)
            serialized_messages = msg_serializer.data
            messages_counter = messages.count()
            current_user_image_serializer = ProfileSerializer.get_profile_image(user_pk=request.user.id)

            cache.set(f'receiver_id.{receiver}: '
                      f'receiver_name.{username}.'
                      f'page.{page}',
                      {'messages': serialized_messages,
                       'message_counter': messages_counter,
                       'current_user_image': current_user_image_serializer},
                      120)
        else:
            serialized_messages = cached_data['messages']
            messages_counter = cached_data['message_counter']
            current_user_image_serializer = cached_data['current_user_image']
            delete_keys_matching_pattern('receiver_id.*')

        return render(request, 'forum/chat.html', context={
            'receiver': receiver,
            'username': username,
            'messages': serialized_messages,
            'page': pagination.get_page,
            'message_counter': messages_counter,
            'current_user_image': current_user_image_serializer
        })
