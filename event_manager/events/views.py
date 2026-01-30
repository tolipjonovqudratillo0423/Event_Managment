from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Event, Ticket, Booking, Category    
from .permissions import IsEventOwner, IsBookingOwner, IsTicketEventOwner,IsVerifiedUser
from .serializers import EventSerializer, TicketSerializer, BookingSerializer, CategorySerializer

# Create your views here.

@extend_schema(tags=["Events"])
class EventViewSet(ModelViewSet):
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        'title',
        'description',
        'location',
        'address',
    ]

    ordering_fields = [
        'start_time',
        'created_at',
    ]

    ordering = ['-created_at']

    def get_permissions(self):
       
        if getattr(self, "action", None) in ("list", "retrieve"):
            return [AllowAny()]
        if getattr(self, "action", None) == "create":
            return [IsAuthenticated(), IsVerifiedUser()]
        return [IsAuthenticated(), IsVerifiedUser(), IsEventOwner()]

    def get_queryset(self):
        qs = super().get_queryset()

        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category_id=category)

        is_active = self.request.query_params.get("is_active")
        if is_active in ("true", "false"):
            qs = qs.filter(is_active=(is_active == "true"))

        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

   
@extend_schema(tags=["Tickets"])   
class TicketViewSet(ModelViewSet):
    
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        # Only event owner can create/update/delete tickets.
        if getattr(self, "action", None) in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsVerifiedUser(), IsTicketEventOwner()]
 
 
@extend_schema(tags=["Categories"])   
class CategoryViewSet(ModelViewSet):
    
    permission_classes = (IsAdminUser, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
 
 
@extend_schema(tags=["Bookings"])   
class BookingViewSet(ModelViewSet):
    
    serializer_class = BookingSerializer
    
    def get_permissions(self):
        
        if getattr(self, "action", None) == "create":
            return [IsAuthenticated(), IsVerifiedUser()]
        return [IsAuthenticated(), IsBookingOwner()]

    def get_queryset(self):
        return Booking.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    

