from django.db import models
from django.contrib.auth.models import User
from django.db import models

class EventsCreated(models.Model):
   event_organizer=models.ForeignKey(User,on_delete=models.CASCADE)
   event_name=models.CharField(max_length=500)
   event_date_time=models.DateTimeField()
   event_maximum_capacity=models.PositiveIntegerField()
   event_ticket_price=models.PositiveIntegerField()
   event_place=models.CharField(max_length=500)
   event_description=models.TextField()
   event_banner=models.ImageField(upload_to='images/', default=None,null=True, blank=True)
   number_of_current_guests=models.PositiveIntegerField()
