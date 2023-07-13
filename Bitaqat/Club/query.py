from datetime import datetime
from Club.models import Event
from django.utils import timezone


def queryEvents(filterby=None, val=None, history=False):
    current_date = datetime.now(tz=timezone.utc)
    if filterby == None:
        list_of_all_events = Event.objects.filter(datetime__gt=current_date)
    else:
        if not history:
            list_of_all_events = Event.objects.all().filter(**
                                                            {filterby: val, "datetime__gt": current_date})
        else:
            list_of_all_events = Event.objects.all().filter(**
                                                            {filterby: val})
    return list_of_all_events
