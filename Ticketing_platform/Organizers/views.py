from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from authentication.models import myUsers
from .models import myOrganizers,EventsCreated,EventsticketsMinted
from django.urls import reverse
from django.http import HttpResponseRedirect
from Organizers.query import queryEvents,countAttandees,loyalty,queryAttEvents
from Guests.models import myGuests
import datetime


# A decorator that checks if the user is logged in. If not, it redirects to the login page.
@login_required(login_url='/login/  ')
def renderHomepage(request):
    print(request.user)
    """
    It takes a request, renders the homepage.html template, and passes the username of the user who made
    the request to the template
    """
    eventNumber=queryEvents('event_organizer_id',request.user.pk)
    attandeesNumber=countAttandees(request.user.pk)
    eventNumberTotal=queryEvents()[1]
    return render(request, 'Organizers\homepage.html', {"user_name": request.user.username,"eventNumber":eventNumber[1],"attandeesNumber":attandeesNumber,"totalEvents":eventNumberTotal})

@login_required(login_url='/login/  ')
def renderProfile(request):
    """
    It takes the user's information from the database and renders it on the profile page. GETTING MYORGANIZER FROM DB
    """
    user_info={}

    user_db=myOrganizers.objects.get(pk=request.user.pk)
    user_info['username']=request.user.username
    user_info['email']=request.user.email
    user_info['Coname']=user_db.Company_name
    return render(request,'Organizers\profile.html',{"data":user_info})

@login_required(login_url='/login/  ')
def renderMarketplace(request):
    all_events=queryEvents()[0]
    print(all_events)
    return render(request,'Organizers\Marketplace.html',{'all_events':all_events})

@login_required(login_url='/login/  ')
def createEvents(request):
    if request.method=='POST':
        event_name_client=request.POST.get('eventname')
        event_date_client=request.POST.get('eventdate')
        event_max_capacity_client=request.POST.get('maxnumber')
        event_ticket_price_client=request.POST.get('price')
        event_place_client=request.POST.get('city')
        event_description_client=request.POST.get('desc')
        event_banner_client=request.FILES['eventimg']
        event_created=EventsCreated(event_organizer=request.user,event_name=event_name_client,event_date_time=event_date_client,event_maximum_capacity=event_max_capacity_client,event_ticket_price=event_ticket_price_client,event_place=event_place_client,event_description=event_description_client,number_of_current_guests=0,event_banner=event_banner_client)
        event_created.save()

        return render(request, 'Organizers\eventcreation.html')
    return render(request, 'Organizers\eventcreation.html')




@login_required(login_url='/login/  ')
def myEvents(request):
    userEventsList=queryEvents('event_organizer',request.user.pk)[0]
    return render(request,'Organizers\ownedEvents.html',{"all_events":userEventsList})
    
    
counter=0

def eventDashboard(request,eventId):
    queryTickets=EventsticketsMinted.objects.filter(**{"event_id":eventId})
    eventQuery=EventsCreated.objects.get(pk=eventId)
    eventData=[]
    loyaltyQuery=loyalty(request.user)
    
    for ticket in queryTickets:
        eventData.append({"ownerName":ticket.NFT_owner_account.username,"ownerAbrev":ticket.NFT_owner_account.username[0]+ticket.NFT_owner_account.username[-1],"ownerEmail":ticket.NFT_owner_account.email,"Token_ID":ticket.NFT_token_id,"loyalty":loyaltyQuery[ticket.NFT_owner_account.username],"ownerID":ticket.NFT_owner_account.pk,"ticket_id":ticket.pk,"checkin":ticket.checkIn_Time})
        print(eventData)
    return render(request,"Organizers\Dashboard.html",{"eventData":eventData,"Number":len(eventData),"Revenue":eventQuery.event_ticket_price*len(eventData),"placesLeft":eventQuery.event_maximum_capacity -len(eventData),"eventName":eventQuery.event_name,"eventBanner":eventQuery.event_banner})
#logout the User
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse("authentication:landingPage"))

def renderAttandedEvents(request,guestID,guestName):
   AttandedEvents=queryAttEvents(guestID,request.user)
   print(AttandedEvents)
   return render(request,'Organizers\AttandedEvents.html',{"attandedEvents":AttandedEvents,"guestName":guestName})
    
def checkInGuest(request,mintedID_DB):
    mintedTicketQuery=EventsticketsMinted.objects.get(pk=mintedID_DB)
    mintedTicketQuery.checkIn_Time=datetime.datetime.now()
    mintedTicketQuery.save()
    return HttpResponseRedirect(reverse("Organizers:eventDashboard",args=(mintedTicketQuery.event_id.pk,)))

