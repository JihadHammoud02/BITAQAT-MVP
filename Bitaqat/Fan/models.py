from django.db import models
from authentication.models import myUsers


class myFan(models.Model):
    user = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True, default=None)
    NFT_Wallet_public_key = models.CharField(max_length=600, default=None)
    NFT_Wallet_private_key = models.CharField(max_length=600, default=None)
    Gas_Wallet_public_key = models.CharField(
        max_length=600, default=None, null=True)
    Gas_Wallet_private_key = models.CharField(
        max_length=600, default=None, null=True)


class QrCodeChecking(models.Model):
    name = models.CharField(max_length=120, default="Qr code")
    description = models.CharField(
        max_length=120, default="This is a Qr code used for check in")
    Qrcode = models.ImageField(
        upload_to='', default=None, null=True, blank=True)
    hash = models.CharField(max_length=300, default=None)
    token_id = models.IntegerField(default=None)
    checked = models.BooleanField(default=False)
    BlockNumber = models.IntegerField(default=None, null=True, blank=True)


class Feedback(models.Model):
    name = models.CharField(max_length=120, default="Qr code")
    email = models.CharField(
        max_length=120, default="This is a Qr code used for check in")
    q1=models.IntegerField(null=True)
    q2=models.IntegerField(null=True)
    q3=models.IntegerField(null=True)
    q4=models.IntegerField(null=True)
    q5=models.IntegerField(null=True)
    q6=models.TextField(null=True)

