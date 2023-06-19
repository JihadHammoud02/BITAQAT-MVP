from django.contrib import admin
from .models import myFan,loyalFan,QrCodeChecking
# Register your models here.

admin.site.register(myFan)
admin.site.register(loyalFan)
admin.site.register(QrCodeChecking)