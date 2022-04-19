from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions
from rest_framework import mixins


from . import models, serializers
from .filters import VehicleFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, MyVehicle, MyVehicleImages


class VehiclesViewSet(ModelViewSet):
    queryset = models.Vehicles.objects.select_related(
        'owner__user').prefetch_related('images').all()
    serializer_class = serializers.VehiclesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VehicleFilter
    ordering_fields = ['price', 'id']
    pagination_class = DefaultPagination
    permission_classes = [MyVehicle]
    search_fields = ['model', 'manufacturer',
                     'description', 'owner__user__first_name']

    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            try:
                return { 'owner_id': self.request.user.seller.id}
            except ObjectDoesNotExist:
                return {'owner_id': None}
        return {'request': self.request}


class VehicleImageViewSet(ModelViewSet):
    serializer_class = serializers.ImageSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated:
            vehicle = models.Vehicles.objects.only('owner').select_related(
                'owner__user').get(id=self.kwargs['vehicle_pk'])
            try:
                if vehicle.owner == self.request.user.seller:
                    return [MyVehicleImages()]
            except ObjectDoesNotExist:
                return [IsAdminOrReadOnly()]
        return [IsAdminOrReadOnly()]

    def get_queryset(self):
        return models.VehicleImage.objects.filter(vehicle_id=self.kwargs['vehicle_pk'])

    def get_serializer_context(self):
        return {'vehicle_id': self.kwargs['vehicle_pk']}


class SellerViewSet(ModelViewSet):
    queryset = models.Seller.objects.prefetch_related(
        'vehicles__images').select_related('user').all()
    serializer_class = serializers.SellerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        (seller, created) = models.Seller.objects.prefetch_related(
            'vehicles__images').select_related('user').get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = serializers.SellerSerializer(seller)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.SellerSerializer(
                seller, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    

class FollowViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    GenericViewSet):
    serializer_class = serializers.FollowSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return models.Follow.objects.filter(seller_id=self.kwargs['seller_pk'])

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'seller_id': self.kwargs['seller_pk']}


class LikeViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = models.Like.objects.prefetch_related('liked_item__vehicle').all()
    serializer_class = serializers.LikeSerializer


class LikedItemViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       GenericViewSet):
    serializer_class = serializers.LikedItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.LikedItem.objects.filter(like_id=self.kwargs['like_pk']).select_related('vehicle')

    def get_serializer_context(self):
        return {'like_id': self.kwargs['like_pk']}
