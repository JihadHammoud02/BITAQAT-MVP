from django.db import models
from authentication.models import myUsers



class myGuests(models.Model):
    user = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True,default=None)
    public_crypto_address=models.CharField(max_length=600,default=None)
    private_crypto_address=models.CharField(max_length=600,default=None)


