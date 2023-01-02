from authentication.models import myUsers
from Guests.models import myGuests
from Organizers.models import EventsCreated
from Organizers.models import ticketsMinted



def queryEvents(filterby=None,val=None):
    if filterby==None:
        list_of_all_events=EventsCreated.objects.all()
    else:
        list_of_all_events=EventsCreated.objects.all().filter(**{filterby:val})
    all_events=[]
    event={}
    for eve in list_of_all_events:
        event['id']=eve.pk
        event['name']=eve.event_name
        event['datetime']=eve.event_date_time.__str__()
        event['desc']=eve.event_description
        event['banner']=eve.event_banner
        event['price']=eve.event_ticket_price
        event['maxcap']=eve.event_maximum_capacity
        event['available_places']=eve.event_maximum_capacity-eve.number_of_current_guests
        event['organizer']=eve.event_organizer
        all_events.append(event)
        event={}
        print(all_events)
    return (all_events,len(all_events))



def queryOrganisers(filterby=None,val=None):
    if filterby==None:
        usersQuery=myUsers.objects.all()
    else:
        usersQuery=myUsers.objects.all().filter(**{filterby:val})
    users=[]
    for user in usersQuery:
        users.append({"username":user.username,"email":user.email,"Coname":user.Compan})



def countAttandees(userId):
    list_of_all_events=EventsCreated.objects.all().filter(**{'event_organizer_id':userId})
    totalAttandees=0;
    for event in list_of_all_events:
        totalAttandees+=event.number_of_current_guests
    return totalAttandees


