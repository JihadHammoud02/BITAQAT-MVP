from authentication.models import myUsers
from Fan.models import myFan,loyalFan
from Club.models import EventsCreated
from Club.models import EventsticketsMinted



def queryEvents(filterby=None,val=None):
    if filterby==None:
        list_of_all_events=EventsCreated.objects.all()
    else:
        list_of_all_events=EventsCreated.objects.all().filter(**{filterby:val})
    all_events=[]
    event={}
    for eve in list_of_all_events:
        event['id']=eve.pk
        event['name1']=eve.Team1Name
        event['name2']=eve.Team2Name
        event['name']=str(event['name1'])+" vs "+str(event['name2'])
        event['date']=str(eve.event_date_time.date())
        event['time']=str(eve.event_date_time.time())[:5]
        event['banner1']=eve.Team1Logo
        event['banner2']=eve.Team2Logo
        event['price']=eve.event_ticket_price
        event['maxcap']=eve.event_maximum_capacity
        event['available_places']=eve.event_maximum_capacity-eve.number_of_current_Fan
        event['organizer']=eve.event_organizer
        event['place2']=eve.event_place
        event['currentNumber']=eve.number_of_current_Fan
        event['category']=eve.category
        all_events.append(event)
        event={}
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
        totalAttandees+=event.number_of_current_Fan
    return totalAttandees


def loyalty(eventOrganizerId):
    loyaltyQuery=loyalFan.objects.filter(**{'organizer':eventOrganizerId})
    loyalData={}
    for attandee in loyaltyQuery:
        loyalData[attandee.guest.username]=attandee.eventsCount
    return loyalData



def queryAttEvents(guestID,organizerID):
    ticketsQuery=EventsticketsMinted.objects.filter(**{'NFT_owner_account':guestID,'organizer':organizerID})
    attandedEventsMetatData=[]
    for tickets in ticketsQuery:
        attandedEventsMetatData.append({'name':str(tickets.event_id.Team1Name)+" vs "+str(tickets.event_id.Team2Name),'banner':tickets.event_id.Team1Name})
    return attandedEventsMetatData
