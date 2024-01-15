from django.db import models
from authentication.models import myUsers


class myFan(models.Model):
    username = models.OneToOneField(myUsers, on_delete=models.CASCADE,
                                primary_key=True, default=None)
    has_received_matic = models.BooleanField(default=False)

class CryptoWallets(models.Model):
    public_key=models.CharField(max_length=600, default=None)
    private_key=models.CharField(max_length=600, default=None)
    username=models.ManyToOneRel(myUsers.username,myUsers,"username",on_delete=models.CASCADE)
    type=models.CharField(max_length=250,default=None)
    class Meta:
        # Define the composite primary key
        unique_together = ('public_key', 'private_key')




class QrCodeChecking(models.Model):
    token_id = models.IntegerField(default=None,primary_key=True)
    checked = models.BooleanField(default=False)


class QrCodeData(models.Model):
    token_id = models.OneToOneField(QrCodeChecking,default=None,on_delete=models.CASCADE)

    name = models.CharField(max_length=120, default="Qr code")

    description = models.CharField(
        max_length=120, default="This is a Qr code used for check in")
    
    Qrcode = models.ImageField(
        upload_to='', default=None, null=True, blank=True)
    
    hash = models.CharField(max_length=300, default=None)



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

