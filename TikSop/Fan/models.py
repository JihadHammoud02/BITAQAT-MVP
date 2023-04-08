from django.db import models
from authentication.models import myUsers
from Club.models import myClub


class myFan(models.Model):
    user = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True,default=None)
    public_crypto_address=models.CharField(max_length=600,default=None)
    private_crypto_address=models.CharField(max_length=600,default=None)


class loyalFan(models.Model):
    guest=models.OneToOneField(myUsers,on_delete=models.CASCADE,
                                default=None,related_name='Fan')
    organizer=models.ForeignKey(myUsers,on_delete=models.CASCADE,
                                default=None,related_name='Club')

    eventsCount=models.IntegerField(default=0)


