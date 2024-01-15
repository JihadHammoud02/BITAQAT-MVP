from django.db import models
from authentication.models import myUsers



class myClub(models.Model):

    username = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True, default=None)
    name = models.CharField(max_length=500, default=None)
    logo = models.ImageField(
        upload_to='ClubsData', max_length=600, default=None, null=True, blank=True)


class Events(models.Model):
    team1 = models.ForeignKey(myClub, on_delete=models.CASCADE,related_name='team1',default=None)
    team2 = models.ForeignKey(myClub, on_delete=models.CASCADE,related_name='team2',default=None)
    datetime = models.DateTimeField(default="2023-09-30 23:02")
    place = models.CharField(max_length=500)
    capacity = models.PositiveIntegerField()
    maximum_ticket_per_account = models.PositiveIntegerField(default=None)
    price = models.FloatField()
    current_fan_count = models.PositiveIntegerField()
    royalty_rate = models.PositiveIntegerField(default=None)
    banner = models.ImageField(
        upload_to='', default="None", null=True, blank=True)
    

# TODO: Add newOwner field to store the current NFT owner from the blockchain and when it changes change the username to None

class MintedTickets(models.Model):
    token_id = models.CharField(max_length=600, default=None,primary_key=True)
    event = models.ForeignKey(
        Events, on_delete=models.CASCADE, related_name='event_id')
    username = models.ForeignKey(
        myUsers, on_delete=models.CASCADE, related_name="event_Attandee", null=True,default=None)
    checked = models.BooleanField(default=False)
    datebought = models.DateTimeField(default="2023-06-30 23:02")
    # newOwner=models.CharField(max_length=600)