from django.contrib import admin
from .models import myClub,EventsticketsMinted,EventsCreated
# Register your models here.

admin.site.register(myClub)
admin.site.register(EventsticketsMinted)
admin.site.register(EventsCreated)