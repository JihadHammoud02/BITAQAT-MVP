from django.contrib import admin
from .models import myFan, QrCodeChecking,CryptoWallets
# Register your models here.

admin.site.register(myFan)
admin.site.register(QrCodeChecking)
admin.site.register(CryptoWallets)
