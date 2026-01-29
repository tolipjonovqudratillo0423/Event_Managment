from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema

from .models import Event, Ticket, Booking, Category    
from .permissions import IsEventOwner, IsBookingOwner, IsTicketEventOwner
from .serializers import EventSerializer, TicketSerializer, BookingSerializer, CategorySerializer

# Create your views here.

@extend_schema(tags=["Events"])
class EventViewSet(ModelViewSet):
    
    permission_classes = (IsAuthenticated, IsEventOwner)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@extend_schema(tags=["Tickets"])   
class TicketViewSet(ModelViewSet):
    
    permission_classes = (IsAuthenticated, IsTicketEventOwner)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
 
 
@extend_schema(tags=["Categories"])   
class CategoryViewSet(ModelViewSet):
    
    permission_classes = (IsAdminUser, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
 
 
@extend_schema(tags=["Bookings"])   
class BookingViewSet(ModelViewSet):
    
    permission_classes = (IsAuthenticated, IsBookingOwner)
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(owner=self.request.user)
    
    

