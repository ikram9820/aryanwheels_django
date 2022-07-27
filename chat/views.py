from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.db.models import Q

from . import serializers
from . import models 
from . import permissions as custom_permissions



class ChatViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = serializers.ChatSerializer
    permission_classes = [custom_permissions.ChatPermission]
    def get_queryset(self):
        user_id = self.request.user.id
        return models.Chat.objects.filter(Q(user1_id = user_id) |  Q(user2_id = user_id) )

    def get_serializer_context(self):
        return {'user_id' :self.request.user.id}


class ChatMessagesViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = serializers.ChatMessagesSerializer
    permission_classes = [custom_permissions.MessagePermmision]

    def get_queryset(self):
        return models.Message.objects.filter(chat_id = self.kwargs['chat_pk'])

    def get_serializer_context(self):
        return {'user_id' :self.request.user.id,'chat_id': self.kwargs['chat_pk']}


