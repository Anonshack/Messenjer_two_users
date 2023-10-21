from collections import namedtuple

from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.views import checkUserToken
from .filters import ChatMessagesFilterBackend

from .models import Chats, Messages
from .serializers import MessagesSerializer, ChatsSerializer, ChatMessagesSerializer

Chat_with_messages = namedtuple('Chat_with_messages', ('chat', 'messages'))


# Create your views here.
class MessageCreateAPIView(CreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer


class ChatCreateAPIView(CreateAPIView):
    queryset = Chats.objects.all()
    serializer_class = ChatsSerializer


class ChatsListAPIView(ListAPIView):
    # queryset = Chats.objects.all()
    serializer_class = ChatsSerializer

    def get_queryset(self):
        user = self.kwargs['user']
        try:
            queryset = Chats.objects.filter(chat_user1=user, is_active=True) | Chats.objects.filter(chat_user2=user, is_active=True)
        except:
            queryset = Chats.objects.none()
        return queryset


class ChatDeleteAPIView(UpdateAPIView):
    serializer_class = None
    def update(self, request, *args, **kwargs):
        try:
            token = request.META['HTTP_TOKEN']
        except:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')

        user = checkUserToken(token)
        if not user:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')

        try:
            chat_id = kwargs['chat_id']
            queryset = Chats.objects.filter(pk=chat_id, chat_user1=request.user.id).update(is_active=False) | Chats.objects.filter(pk=chat_id, chat_user2=request.user.id).update(is_active=False)
            return Response({'detail': 'Deleted'})
        except:
            return Response({'detail': 'Unexpected error'})


class ChatMessagesListAPIView(ListAPIView):
    # serializer_class = ChatMessagesSerializer
    filter_backends = (ChatMessagesFilterBackend,)

    def list(self, request, *args, **kwargs):
        try:
            user_1 = request.GET['user_1']
            user_2 = request.GET['user_2']
            # print(f"User1: {user_1},\tUSer2: {user_2}")
            chat_queryset = Chats.objects.filter(chat_user1=user_1, chat_user2=user_2, is_active=True) | Chats.objects.filter(chat_user1=user_2, chat_user2=user_1, is_active=True)
            # print(chat_queryset[0].started_time)
            messages_queryset = Messages.objects.filter(message_chat=chat_queryset[0].id, message_status=True)
            # print(messages_queryset)
            chat_with_messages = Chat_with_messages(
                chat=chat_queryset,
                messages=messages_queryset
            )
            serializer=ChatMessagesSerializer(chat_with_messages)
            return Response(serializer.data)
        except:
            return Response({'detail': 'invalid'})


@api_view(['POST'])
def setReactionAPIView(request, msg_id, reaction):
        try:
            token = request.META['HTTP_TOKEN']
        except:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')

        user = checkUserToken(token)
        if not user:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')

        msg_react_status = Messages.objects.filter(pk=msg_id, message_status=True).exclude(message_user=request.user.id).values_list('message_reaction').first()

        if msg_react_status is None:
            Messages.objects.filter(pk=msg_id).update(message_reaction=reaction)
            return Response({'detail': 'Reaction set', 'reaction': reaction})

        if msg_react_status[0] == bool(reaction):
            Messages.objects.filter(pk=msg_id).update(message_reaction=None)
            return Response({'detail': 'Reaction canceled', 'reaction': None})

        if reaction:
            Messages.objects.filter(pk=msg_id).update(message_reaction=True)
            return Response({'detail': 'Liked'})

        Messages.objects.filter(pk=msg_id).update(message_reaction=False)
        return Response({'detail': 'Disliked'})