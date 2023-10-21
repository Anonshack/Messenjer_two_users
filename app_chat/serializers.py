from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer

from .models import Chats, Messages


class MessagesSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = ['id', 'message_chat', 'message_text', 'message_image', 'message_datetime', 'message_user', 'message_status', 'message_reaction']
        extra_kwargs = {
            'id': {'read_only': True},
            'message_reaction': {'read_only': True},
            'message_status': {'read_only': True}
        }


class ChatsSerializer(ModelSerializer):
    class Meta:
        model = Chats
        fields = ['id', 'chat_user1', 'chat_user2', 'started_time']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ChatMessagesSerializer(Serializer):
    chat = ChatsSerializer(many=True)
    messages = MessagesSerializer(many=True)