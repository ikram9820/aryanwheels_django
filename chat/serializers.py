from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from . import models


class ChatSerializer(serializers.ModelSerializer):
    user1_id = serializers.IntegerField(read_only = True)
    user2_id = serializers.IntegerField()
    at = serializers.DateTimeField(read_only = True)
    class Meta:
        model = models.Chat 
        fields = ['id','user1_id','user2_id','at']
    
    def create(self, validated_data):
        user1_id = self.context['user_id']
        user2_id = validated_data['user2_id']
        try:
            return models.Chat.objects.get(Q(user1_id = user1_id) & Q(user2_id= user2_id) | Q(user1_id = user2_id) & Q(user2_id= user1_id) )
        except ObjectDoesNotExist:
            return models.Chat.objects.create(user1_id = user1_id,**validated_data)


class ChatMessagesSerializer(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(read_only = True)
    author = serializers.StringRelatedField(read_only = True)
    texted_at = serializers.DateTimeField(read_only = True)
    class Meta:
        model = models.Message
        fields = ['id','chat_id','author','texted_at','text']

    def create(self, validated_data):
        chat_id = self.context['chat_id']
        user_id = self.context['user_id']
        return models.Message.objects.create(chat_id=chat_id,author_id= user_id, **validated_data)
