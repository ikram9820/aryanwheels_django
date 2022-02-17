from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
     def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)



class MyVehicle(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET','HEAD','OPTIONS']:
            return True
        # elif request.method == ['POST']:
        return bool(request.user and bool(request.user.is_staff or request.user.is_authenticated))
        
    def has_object_permission(self, request, view, obj):
        if request.method in['GET','HEAD','OPTIONS']:
            return True
        return  bool((obj.owner == request.user.seller) and request.user )


class MyVehicleImages(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET','HEAD','OPTIONS']:
            return True
        return bool(request.user and (request.user.is_staff or request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        if request.method in['GET','HEAD','OPTIONS']:
            return True
        return  bool((obj.vehicle.owner == request.user.seller) and request.uesr)

