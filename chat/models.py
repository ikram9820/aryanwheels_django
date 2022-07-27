from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user1_chat')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user2_chat')
    at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [['user1','user2']]
        ordering = ['at']

class Message(models.Model):
    texted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='message')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='send_text')

    def __str__(self) -> str:
        return self.author.username
        
    class Meta:
        ordering = ['texted_at']