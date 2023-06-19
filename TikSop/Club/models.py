from django.db import models
from authentication.models import myUsers

class myClub(models.Model):
    user = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True,default=None)
    Number_of_events_created=models.PositiveIntegerField(default=0)
    Company_name=models.CharField(max_length=250,default=None)
    RoyaltyReceiverAddresse=models.CharField(max_length=500,default=None)


class EventsCreated(models.Model):
   EventBanner=models.ImageField(upload_to='', default=None,null=True, blank=True)
   event_organizer=models.ForeignKey(myUsers,on_delete=models.CASCADE)
   Team1Name=models.CharField(max_length=500,default=None)
   Team2Name=models.CharField(max_length=500,default=None)
   event_date_time=models.DateTimeField()
   event_maximum_capacity=models.PositiveIntegerField()
   event_ticket_price=models.FloatField()
   event_place=models.CharField(max_length=500)
   Team1Logo=models.ImageField(upload_to='', default=None,null=True, blank=True)
   Team2Logo=models.ImageField(upload_to='', default=None,null=True, blank=True)
   number_of_current_Fan=models.PositiveIntegerField()
   royaltyRate=models.PositiveIntegerField(default=None)
   SecondarySalesRules=models.CharField(max_length=500,default=None)
   SecondarySalesCapPrice=models.PositiveIntegerField(null=True,default=None)
   category=models.CharField(max_length=500,default=None,null=True,blank=True)




class EventsticketsMinted(models.Model):
   event_id=models.ForeignKey(EventsCreated,on_delete=models.CASCADE,related_name='event_id')
   event_name=(str(EventsCreated.Team1Name)+" vs "+str(EventsCreated.Team2Name))
   NFT_owner_address=models.CharField(max_length=600,default=None)
   NFT_owner_account=models.ForeignKey(myUsers,on_delete=models.CASCADE,related_name="event_Attandee")
   NFT_token_id=models.CharField(max_length=600,default=None)
   organizer=models.ForeignKey(myUsers,on_delete=models.CASCADE,
                                related_name="event_organizer",default=0)
   checkIn_Time=models.TimeField(null=True,blank=True)
   TimeStamp=models.TimeField(null=True,blank=True)
   datebought=models.DateField(null=True,blank=True)



class SportCategories(models.Model):
   name=models.CharField(max_length=500,default=None)


class clubData(models.Model):
   clubId=models.ForeignKey(myUsers,on_delete=models.CASCADE,related_name="clubId")
   stadiumImage=models.ImageField(upload_to='', default=None,null=True, blank=True)
   teamLogo=models.ImageField(upload_to='', default=None,null=True, blank=True)
   clubName=models.CharField(max_length=600,default=None)
