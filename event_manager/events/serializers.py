from rest_framework import serializers

from .models import Event, Ticket, Booking, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
     
        

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ('id','is_active','owner','created_at','updated_at',)
     
        


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ('id','is_active','created_at','updated_at',)
        


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ('id','is_active','owner','created_at','updated_at',)
        

