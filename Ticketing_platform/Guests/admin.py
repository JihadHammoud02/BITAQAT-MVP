from django.contrib import admin
from .models import myGuests,loyalGuests
# Register your models here.

admin.site.register(myGuests)
admin.site.register(loyalGuests)