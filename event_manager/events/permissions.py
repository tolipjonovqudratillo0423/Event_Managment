from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEventOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.owner
    
class IsBookingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsTicketEventOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.event.owner == request.user