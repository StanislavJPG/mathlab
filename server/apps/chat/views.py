from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Q, F, When, Case, CharField, OuterRef, Subquery

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from server.apps.chat.models import Message
from server.apps.chat.serializer import MessageSerializer
from server.apps.forum.utils import PaginationCreator, delete_keys_matching_pattern
from server.apps.users.serializers import ProfileSerializer


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, receiver: int, username: str):
        page = request.GET.get("page")
        cached_data = cache.get(
            f"receiver_id.{receiver}: receiver_name.{username}.page.{page}"
        )
        pagination = PaginationCreator(page, limit=8)
        offset = pagination.get_offset

        if not cached_data:
            messages = Message.objects.filter(
                sender__in=[request.user.id, receiver],
                receiver__in=[request.user.id, receiver],
            ).order_by("-sent_at")[offset : offset + 8]

            msg_serializer = MessageSerializer(messages, many=True)
            serialized_messages = msg_serializer.data
            messages_counter = messages.count()
            current_user_image_serializer = ProfileSerializer.get_profile_image(
                user_pk=request.user.id
            )

            cache.set(
                f"receiver_id.{receiver}: receiver_name.{username}.page.{page}",
                {
                    "messages": serialized_messages,
                    "message_counter": messages_counter,
                    "current_user_image": current_user_image_serializer,
                },
                120,
            )
        else:
            serialized_messages = cached_data["messages"]
            messages_counter = cached_data["message_counter"]
            current_user_image_serializer = cached_data["current_user_image"]
            delete_keys_matching_pattern("receiver_id.*")

        return render(
            request,
            "forum/chat.html",
            context={
                "receiver": receiver,
                "username": username,
                "messages": serialized_messages,
                "page": pagination.get_page,
                "message_counter": messages_counter,
                "current_user_image": current_user_image_serializer,
            },
        )


class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = request.GET.get("page")
        pagination = PaginationCreator(page, limit=10)
        offset = pagination.get_offset
        cached_data = cache.get(f"chat_list.{page}")

        if not cached_data:
            current_user_image_serializer = ProfileSerializer.get_profile_image(
                user_pk=request.user.id
            )

            latest_messages_subquery = (
                Message.objects.filter(
                    Q(sender=OuterRef("sender")) & Q(receiver=OuterRef("receiver"))
                    | Q(sender=OuterRef("receiver")) & Q(receiver=OuterRef("sender"))
                )
                .annotate(
                    sender_username=F("sender__username"),
                )
                .order_by("-sent_at")
                .values("message", "sent_at", "receiver", "sender_username")[:1]
            )

            users_chats = (
                Message.objects.filter(
                    Q(sender=request.user.id) | Q(receiver=request.user.id)
                )
                .annotate(
                    chatroom_user1=Case(
                        When(
                            sender__username__lt=F("receiver__username"),
                            then=F("sender__username"),
                        ),
                        default=F("receiver__username"),
                        output_field=CharField(),
                    ),
                    chatroom_user2=Case(
                        When(
                            sender__username__lt=F("receiver__username"),
                            then=F("receiver__username"),
                        ),
                        default=F("sender__username"),
                        output_field=CharField(),
                    ),
                    latest_message=Subquery(latest_messages_subquery.values("message")),
                    sent_at_last_message=Subquery(
                        latest_messages_subquery.values("sent_at")
                    ),
                    receiver_pk=Subquery(latest_messages_subquery.values("receiver")),
                    sender_username=Subquery(
                        latest_messages_subquery.values("sender_username")
                    ),
                )
                .values(
                    "receiver_pk",
                    "sent_at_last_message",
                    "sender_username",
                    "latest_message",
                    "chatroom_user1",
                    "chatroom_user2",
                )
                .distinct()[offset : offset + 10]
            )
            context = {
                "all_chats": users_chats,
                "page": int(page) if page else 1,
                "current_user_image": current_user_image_serializer,
            }
            cache.set(f"chat_list.{page}", context, 60)
        else:
            context = cached_data

        return render(request, "forum/chat_list.html", context=context)
