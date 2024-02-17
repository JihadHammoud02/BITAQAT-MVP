from django.db import models
from authentication.models import myUsers


class ClubsData(models.Model):
    name = models.CharField(max_length=500, default=None)
    logo = models.ImageField(
        upload_to='ClubsData', max_length=600, default=None, null=True, blank=True)


class myClub(models.Model):

    user = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True, default=None)
    club = models.OneToOneField(ClubsData, on_delete=models.CASCADE,
                                default=None)
    RoyaltyReceiverAddresse = models.CharField(max_length=500, null=True)
    RoyaltyReceiver_private_key = models.CharField(max_length=500, null=True)


class Event(models.Model):
    organizer = models.ForeignKey(myClub, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default="2023-09-30 23:02")
    place = models.CharField(max_length=500)
    maximum_capacity = models.PositiveIntegerField()
    maximum_ticket_per_account = models.PositiveIntegerField(default=None)
    ticket_price = models.FloatField()
    current_fan_count = models.PositiveIntegerField()
    royalty_rate = models.PositiveIntegerField(default=None)
    banner = models.ImageField(
        upload_to='EventsBanner', default="None", null=True, blank=True)
    opposite_team = models.ForeignKey(ClubsData, on_delete=models.CASCADE)


class MintedTickets(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='event_id')
    owner_account = models.ForeignKey(
        myUsers, on_delete=models.CASCADE, related_name="event_Attandee", null=True)
    owner_crypto_address = models.CharField(max_length=600, default=None)
    token_id = models.CharField(max_length=600, default=None)
    organizer = models.ForeignKey(myClub, on_delete=models.CASCADE,
                                  related_name="event_organizer", default=0)
    checked = models.BooleanField(default=False)
    datebought = models.DateTimeField(default="2023-06-30 23:02")
