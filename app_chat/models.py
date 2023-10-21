from django.db import models

from django.contrib.auth import get_user_model


# Create your models here.
class Chats(models.Model):
    chat_user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user1')
    chat_user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user2')
    started_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(verbose_name='Chat closed time', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Status of chat', default=True)

    class Meta:
        db_table = 'chats'
        ordering = ['started_time']


class Messages(models.Model):
    message_chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    message_text = models.CharField(max_length=140)
    message_image = models.ImageField(upload_to='images', null=True, blank=True)
    message_datetime = models.DateTimeField(auto_now_add=True)
    message_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message_status = models.BooleanField(default=True)
    message_reaction = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'chats_messages'
        ordering = ['message_datetime']