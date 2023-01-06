from django.db import models
from authentication.models import myUsers
import datetime

class myOrganizers(models.Model):
    user = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True,default=None)
    Number_of_events_created=models.PositiveIntegerField(default=0)
    Company_name=models.CharField(max_length=250,default=None)


class EventsCreated(models.Model):
   event_organizer=models.ForeignKey(myUsers,on_delete=models.CASCADE)
   event_name=models.CharField(max_length=500)
   event_date_time=models.DateTimeField()
   event_maximum_capacity=models.PositiveIntegerField()
   event_ticket_price=models.FloatField()
   event_place=models.CharField(max_length=500)
   event_description=models.TextField()
   event_banner=models.ImageField(upload_to='', default=None,null=True, blank=True)
   number_of_current_guests=models.PositiveIntegerField()




class EventsticketsMinted(models.Model):
   event_id=models.ForeignKey(EventsCreated,on_delete=models.CASCADE,related_name='event_id')
   event_name=EventsCreated.event_name
   NFT_owner_address=models.CharField(max_length=600,default=None)
   NFT_owner_account=models.ForeignKey(myUsers,on_delete=models.CASCADE,related_name="event_Attandee")
   NFT_token_id=models.CharField(max_length=600,default=None)
   organizer=models.ForeignKey(myUsers,on_delete=models.CASCADE,
                                related_name="event_organizer",default=0)
   checkIn_Time=models.TimeField(null=True,blank=True)





