from rest_framework import permissions
from . import models

class ChatPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
 

    def has_object_permission(self, request, view, obj):       
        user_id = request.user.id
        return bool(obj.user1.id == user_id or obj.user2.id == user_id)  

class MessagePermmision(permissions.BasePermission):
     
    def has_permission(self, request, view):
        user = request.user
        if bool(
            user and user.is_authenticated
        ):  
            chat_pk = int(view.kwargs['chat_pk'])
            chat = models.Chat.objects.get(pk = chat_pk)
            return bool(chat.user1.pk == user.id or chat.user2.id == user.id)


    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            request.method in permissions.SAFE_METHODS or
            user and user.is_authenticated and bool(obj.author_id == user.id)
        )
