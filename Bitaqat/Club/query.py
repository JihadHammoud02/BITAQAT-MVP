from authentication.models import myUsers
from Fan.models import myFan
from Club.models import Event
from Club.models import MintedTickets


def queryEvents(filterby=None, val=None):
    if filterby == None:
        list_of_all_events = Event.objects.all()
    else:
        list_of_all_events = Event.objects.all().filter(**
                                                        {filterby: val})
    all_events = []
    event = {}
    for eve in list_of_all_events:
        event['id'] = eve.pk
        event['img'] = eve.banner

        event['date'] = str(eve.datetime.date())
        event['time'] = str(eve.datetime.time())[:5]
        event['price'] = eve.ticket_price
        event['maxcap'] = eve.maximum_capacity
        event['available_places'] = eve.maximum_capacity - \
            eve.current_fan_count
        event['organizer'] = eve.organizer
        event['opposite'] = eve.opposite_team
        event['place2'] = eve.place
        event['currentNumber'] = eve.current_fan_count
        event['name1'] = event['organizer'].club.name
        event['logo'] = event['organizer'].club.logo
        event['name2'] = event['opposite'].name
        event['banner2'] = event['opposite'].logo
        event['name'] = str(event['name1'])+" vs "+str(event['name2'])
        all_events.append(event)
        event = {}
    return (all_events, len(all_events))


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
