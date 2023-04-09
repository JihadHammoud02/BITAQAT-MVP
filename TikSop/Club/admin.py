from django.contrib import admin
from .models import myClub,EventsticketsMinted,EventsCreated,SportCategories,clubData
# Register your models here.

admin.site.register(myClub)
admin.site.register(EventsticketsMinted)
admin.site.register(EventsCreated)
admin.site.register(SportCategories)
admin.site.register(clubData)