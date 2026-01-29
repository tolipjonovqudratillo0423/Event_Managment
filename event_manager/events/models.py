from django.db import models

from django.conf import settings

# Create your models here.
class TicketStatus(models.TextChoices):
    
    ACTIVE, EXPIRED = (('active','Active'),('expired','Expired'))



class Category(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name



class Event(models.Model):
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events', on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name='events', on_delete=models.CASCADE)
    
    title = models.CharField(max_length=1000)
    description = models.TextField()
    contact_phone = models.CharField(max_length=13)
    contact_email = models.EmailField(max_length=150)
    location = models.CharField(max_length=1400)
    address = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title



class Ticket(models.Model):
    
    event = models.ForeignKey(Event, related_name="tickets", on_delete=models.CASCADE)
    
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Ticket for >>> {self.event.title}"
    


class Booking(models.Model):
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="bookings", on_delete=models.CASCADE)
    ticket = models.ForeignKey("Ticket", related_name="bookings", on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField()
    status = models.CharField(choices=TicketStatus.choices, default=TicketStatus.ACTIVE,max_length=50)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"booking of {self.owner.email} "
    