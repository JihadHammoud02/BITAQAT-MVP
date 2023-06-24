from django.db import models
from authentication.models import myUsers


class myClub(models.Model):
    user = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True, default=None)
    Number_of_events_created = models.PositiveIntegerField(default=0)
    Company_name = models.CharField(max_length=250, default=None)


class Event(models.Model):
    organizer = models.ForeignKey(myUsers, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    place = models.CharField(max_length=500)
    maximum_capacity = models.PositiveIntegerField()
    ticket_price = models.FloatField()
    current_fan_count = models.PositiveIntegerField()
    royalty_rate = models.PositiveIntegerField(default=None)
    banner = models.ImageField(
        upload_to='', default=None, null=True, blank=True)
    team1_name = models.CharField(max_length=500, default=None)
    team2_name = models.CharField(max_length=500, default=None)
    team1_logo = models.ImageField(
        upload_to='', default=None, null=True, blank=True)
    team2_logo = models.ImageField(
        upload_to='', default=None, null=True, blank=True)


class MintedTickets(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='event_id')
    owner_account = models.ForeignKey(
        myUsers, on_delete=models.CASCADE, related_name="event_Attandee")
    owner_crypto_address = models.CharField(max_length=600, default=None)
    token_id = models.CharField(max_length=600, default=None)
    organizer = models.ForeignKey(myUsers, on_delete=models.CASCADE,
                                  related_name="event_organizer", default=0)
