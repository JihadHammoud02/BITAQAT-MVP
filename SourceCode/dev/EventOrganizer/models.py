from django.db import models

# Create your models here.
from django.db import models

class EventsCreated(models.Model):

   event_name=models.CharField(max_length=500)
   event_date_time=models.DateTimeField()
   event_maximum_capacity=models.PositiveIntegerField()
   event_ticket_price=models.PositiveIntegerField()
   event_place=models.CharField(max_length=500)
   event_description=models.TextField()
   number_of_current_guests=models.PositiveIntegerField()
