from django.contrib import admin
from .models import myClub, MintedTickets, Event, ClubsData
# Register your models here.

admin.site.register(myClub)
admin.site.register(MintedTickets)
admin.site.register(Event)
admin.site.register(ClubsData)
