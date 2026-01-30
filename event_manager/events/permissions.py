from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import StatusChoices

class IsEventOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.owner
    


class IsBookingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
    
    
class IsTicketEventOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        event_id = request.data.get('event')
        if not event_id:
            return False
        from .models import Event
        return Event.objects.filter(id=event_id, owner=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.event.owner == request.user  
    


class IsVerifiedUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.status in (StatusChoices.VERIFIED, StatusChoices.DONE)
        )