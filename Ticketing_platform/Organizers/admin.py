from django.contrib import admin
from .models import myOrganizers,EventsticketsMinted,EventsCreated
# Register your models here.

admin.site.register(myOrganizers)
admin.site.register(EventsticketsMinted)
admin.site.register(EventsCreated)