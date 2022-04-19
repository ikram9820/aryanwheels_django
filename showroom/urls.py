
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()

router.register('vehicles', views.VehiclesViewSet, basename='vehicles')
router.register('seller', views.SellerViewSet, basename='seller')
router.register('like', views.LikeViewSet, basename='like')

vehicle_router = routers.NestedDefaultRouter(
    router, 'vehicles', lookup='vehicle')
vehicle_router.register(
    'images', views.VehicleImageViewSet, basename='vehicle-images')

like_router = routers.NestedDefaultRouter(router, 'like', lookup='like')
like_router.register('likes', views.LikedItemViewSet, basename='like-vehicles')

seller_router = routers.NestedDefaultRouter(router, 'seller', lookup='seller')
seller_router.register('follow', views.FollowViewSet, basename='seller-follow')

urlpatterns = router.urls + like_router.urls + \
    vehicle_router.urls + seller_router.urls
