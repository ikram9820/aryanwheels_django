from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()

router.register('', views.ChatViewSet, basename='chats')

chat_router = routers.NestedDefaultRouter(router,'',lookup = 'chat')
chat_router.register('messages',views.ChatMessagesViewSet,basename = 'chat-messages')

urlpatterns = router.urls + chat_router.urls