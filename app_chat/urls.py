from django.urls import path

from .views import (
    MessageCreateAPIView,
    ChatCreateAPIView,
    ChatsListAPIView,
    ChatDeleteAPIView,
    ChatMessagesListAPIView,
    setReactionAPIView,
)

chat_urlpatterns = [
    path('new-chat', ChatCreateAPIView.as_view()),
    path('chat/messages', ChatMessagesListAPIView.as_view()),
    path('chats/<int:user>', ChatsListAPIView.as_view()),
    path('chats/delete/<int:chat_id>', ChatDeleteAPIView.as_view())
]

message_urlpatterns = [
    path('new-message', MessageCreateAPIView.as_view()),
    path('message/react/<int:msg_id>/<int:reaction>', setReactionAPIView),
]

urlpatterns = chat_urlpatterns + message_urlpatterns