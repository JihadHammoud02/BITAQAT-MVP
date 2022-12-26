from django.db import models
from django.contrib.auth.models import User
from django.db import models




class EventsCreated(models.Model):
   event_organizer=models.ForeignKey(User,on_delete=models.CASCADE)
   event_name=models.CharField(max_length=500)
   event_date_time=models.DateTimeField()
   event_maximum_capacity=models.PositiveIntegerField()
   event_ticket_price=models.FloatField()
   event_place=models.CharField(max_length=500)
   event_description=models.TextField()
   event_banner=models.ImageField(upload_to='', default=None,null=True, blank=True)
   number_of_current_guests=models.PositiveIntegerField()



class ticketsMinted(models.Model):
   event_id=models.ForeignKey(EventsCreated,on_delete=models.CASCADE)
   event_name=EventsCreated.event_name
   NFT_owner_address=models.CharField(max_length=600,default=None)
   NFT_owner_account=models.CharField(max_length=600,default=None)
