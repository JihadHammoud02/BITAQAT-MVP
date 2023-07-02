from datetime import datetime
from Club.models import Event
from Club.models import MintedTickets


def queryEvents(filterby=None, val=None, history=False):
    current_date = datetime.now()
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


def queryOrganisers(filterby=None, val=None):
    if filterby == None:
        myUsersQuery = myUsers.objects.all()
    else:
        myUsersQuery = myUsers.objects.all().filter(**{filterby: val})
    myUsers = []
    for user in myUsersQuery:
        myUsers.append({"username": user.username,
                       "email": user.email, "Coname": user.Compan})


def countAttandees(userId):
    list_of_all_events = Event.objects.all().filter(
        **{'organizer_id': userId})
    totalAttandees = 0
    for event in list_of_all_events:
        totalAttandees += event.current_fan_count
    return totalAttandees


def queryAttEvents(guestID, organizerID):
    ticketsQuery = MintedTickets.objects.filter(
        **{'owner_account': guestID, 'organizer': organizerID})
    attandedEventsMetatData = []
    for tickets in ticketsQuery:
        attandedEventsMetatData.append({'name': str(tickets.event_id.team1_name)+" vs "+str(
            tickets.event_id.team2_name), 'banner': tickets.event_id.team1_name})
    return attandedEventsMetatData
