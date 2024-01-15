from django.contrib import admin
from .models import myClub, MintedTickets, Events
# Register your models here.

admin.site.register(myClub)
admin.site.register(MintedTickets)
admin.site.register(Events)
