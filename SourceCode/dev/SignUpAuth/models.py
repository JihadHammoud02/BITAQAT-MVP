from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Organizers(models.Model):

    User._meta.get_field('email')._unique = True
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True,)
    nationnality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)


class Attandees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True,)
    nationnality = models.CharField(max_length=200)
    public_crypto_address=models.CharField(max_length=600,default=None)
    private_crypto_address=models.CharField(max_length=600,default=None)
    city = models.CharField(max_length=200)
