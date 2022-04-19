from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
class IsAdminOrReadOnly(permissions.BasePermission):
     def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class MyVehicle(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET','HEAD','OPTIONS']:
            return True
        
        try:
            return bool(request.user.seller and bool(request.user.is_staff or request.user.is_authenticated))
        except Exception as e:
            print(f"this exception is occured in has_permission function of MyVehicle permisions  {e}")
            return False
        
    def has_object_permission(self, request, view, obj):
        if request.method in['GET','HEAD','OPTIONS']:
            return True
        try:
            return  bool((obj.owner == request.user.seller) and request.user )
        except Exception as e:
            print(f"this exception is occured in has_object_permission function of MyVehicle permisions  {e}")
            return False


class MyVehicleImages(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET','HEAD','OPTIONS']:
            return True
        try:
            return bool(request.user.seller and bool(request.user.is_staff or request.user.is_authenticated))
        except Exception as e:
            print(f"this exception is occured in has_permission function of MyVehicleImages permisions  {e}")
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in['GET','HEAD','OPTIONS']:
            return True
        try:
            return  bool((obj.vehicle.owner == request.user.seller) and request.user)
        except Exception as e:
            print(f"this exception is occured in has_object_permission function of MyVehicleImages permisions  {e}")
            return False

