from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from authentication.models import myUsers
from .models import myClub,EventsCreated,EventsticketsMinted,SportCategories,clubData
from django.urls import reverse
from django.http import HttpResponseRedirect
from Club.query import queryEvents,countAttandees,loyalty,queryAttEvents
from Fan.models import myFan
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
    return render(request, 'Club\homepage.html', {"user_name": request.user.username,"eventNumber":eventNumber[1],"attandeesNumber":attandeesNumber,"totalEvents":eventNumberTotal})

@login_required(login_url='/login/  ')
def renderProfile(request):
    """
    It takes the user's information from the database and renders it on the profile page. GETTING MYORGANIZER FROM DB
    """
    user_info={}

    user_db=myClub.objects.get(pk=request.user.pk)
    user_info['username']=request.user.username
    user_info['email']=request.user.email
    user_info['Coname']=user_db.Company_name
    return render(request,'Club\profile.html',{"data":user_info})

@login_required(login_url='/login/  ')
def renderMarketplace(request):
    all_events=queryEvents()[0]
    print(all_events)
    return render(request,'Club\Marketplace.html',{'all_events':all_events})

@login_required(login_url='/login/  ')
def createEvents(request):
    CategoriesQuery=SportCategories.objects.all()
    Category=[]
    for category in CategoriesQuery:
        Category.append(category.name)
    if request.method=='POST':
        category2=request.POST.get('categorie')
        Team1name1=request.POST.get('name1')
        Team2name2=request.POST.get('name2')
        Team1logo1=request.FILES['logo1']
        Team2logo2=request.FILES['logo2']
        game_date_client=request.POST.get('eventdate')
        game_max_capacity_client=request.POST.get('maxnumber')
        game_ticket_price_client=request.POST.get('price')
        game_place_client=request.POST.get('city')
        SecondaryMR=request.POST.getlist('check')
        SecondaryMRN=request.POST.get('capnumber')
        royalty=request.POST.get('royap')
        
        event_created=EventsCreated(event_organizer=request.user,Team1Name=Team1name1,Team2Name=Team2name2,Team1Logo=Team1logo1,Team2Logo=Team2logo2,event_date_time=game_date_client,event_maximum_capacity=game_max_capacity_client,event_ticket_price=game_ticket_price_client,event_place=game_place_client,number_of_current_Fan=0,royaltyRate=royalty,SecondarySalesRules=SecondaryMR,SecondarySalesCapPrice=SecondaryMRN,category=category2)
        event_created.save()

        return render(request, 'Club\eventcreation.html')
    return render(request, 'Club\eventcreation.html',{"categories":Category})




@login_required(login_url='/login/  ')
def myEvents(request):
    userEventsList=queryEvents('event_organizer',request.user.pk)[0]
    return render(request,'Club\ownedEvents.html',{"all_events":userEventsList})
    
    
counter=0

def eventDashboard(request,eventId):
    queryTickets=EventsticketsMinted.objects.filter(**{"event_id":eventId})
    eventQuery=EventsCreated.objects.get(pk=eventId)
    eventData=[]
    loyaltyQuery=loyalty(request.user)
    
    for ticket in queryTickets:
        eventData.append({"ownerName":ticket.NFT_owner_account.username,"ownerAbrev":ticket.NFT_owner_account.username[0]+ticket.NFT_owner_account.username[-1],"ownerEmail":ticket.NFT_owner_account.email,"Token_ID":ticket.NFT_token_id,"loyalty":loyaltyQuery[ticket.NFT_owner_account.username],"ownerID":ticket.NFT_owner_account.pk,"ticket_id":ticket.pk,"checkin":ticket.checkIn_Time})
        print(eventData)
    return render(request,"Club\Dashboard.html",{"eventData":eventData,"Number":len(eventData),"Revenue":eventQuery.event_ticket_price*len(eventData),"placesLeft":eventQuery.event_maximum_capacity -len(eventData),"eventName":eventQuery.event_name,"eventBanner":eventQuery.event_banner})
#logout the User
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse("authentication:landingPage"))

def renderAttandedEvents(request,guestID,guestName):
   AttandedEvents=queryAttEvents(guestID,request.user)
   print(AttandedEvents)
   return render(request,'Club\AttandedEvents.html',{"attandedEvents":AttandedEvents,"guestName":guestName})
    
def checkInGuest(request,mintedID_DB):
    mintedTicketQuery=EventsticketsMinted.objects.get(pk=mintedID_DB)
    mintedTicketQuery.checkIn_Time=datetime.datetime.now()
    mintedTicketQuery.save()
    return HttpResponseRedirect(reverse("Club:eventDashboard",args=(mintedTicketQuery.event_id.pk,)))

def getClubData(request):
    query_clubData=clubData.objects.filter(**{"clubId":request.user.pk})
    
    if request.method=='POST':
        cname=request.POST.get('name1')
        clogo=request.FILES['logo1']
        cstadium=request.FILES['stad']

        RegisterDb=clubData(clubId=request.user,stadiumImage=cstadium,teamLogo=clogo,clubName=cname)
        RegisterDb.save()
    else:
        
        if len(query_clubData)!=0:
            stadium=query_clubData[len(query_clubData)-1].stadiumImage
            name=query_clubData[len(query_clubData)-1].clubName
            logo=query_clubData[len(query_clubData)-1].teamLogo
            container={"stadium":stadium,"name":name,"logo":logo}
            print('yes')
            return render(request,'Club\MyClub.html',{"data":container})
    return render(request,'Club\MyClub.html')