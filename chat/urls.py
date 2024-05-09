from django.urls import path

from chat.views import ChatView

urlpatterns = [
    path('chat/communication/<int:user_id>/<str:username>', ChatView.as_view(), name='ws-chat')
]
