from django.contrib import admin
from . import models 
# Register your models here.



class ChatMessagesInline(admin.TabularInline):
    model = models.Message


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['user1','user2','at']
    inlines = [ChatMessagesInline]
    list_per_page = 10

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['author','author_id','chat','text','texted_at',]
    search_fields = ['text']
    list_editable = ['text']
    list_per_page = 10
