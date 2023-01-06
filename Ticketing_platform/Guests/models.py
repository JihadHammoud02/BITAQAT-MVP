from django.db import models
from authentication.models import myUsers
from Organizers.models import myOrganizers


class myGuests(models.Model):
    user = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True,default=None)
    public_crypto_address=models.CharField(max_length=600,default=None)
    private_crypto_address=models.CharField(max_length=600,default=None)


class loyalGuests(models.Model):
    guest=models.OneToOneField(myUsers,on_delete=models.CASCADE,
                                default=None,related_name='guests')
    organizer=models.ForeignKey(myUsers,on_delete=models.CASCADE,
                                default=None,related_name='organizers')

    eventsCount=models.IntegerField(default=0)


