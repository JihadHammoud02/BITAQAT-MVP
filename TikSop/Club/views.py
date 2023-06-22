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
from Fan.utils import getOwners,VolumneTraded
import time
from Fan.SmartContract import get_balance
from datetime import datetime, timedelta
from Fan.models import QrCodeChecking
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
        banner=request.POST.get('banner')
        
        event_created=EventsCreated(event_organizer=request.user,Team1Name=Team1name1,Team2Name=Team2name2,Team1Logo=Team1logo1,Team2Logo=Team2logo2,event_date_time=game_date_client,event_maximum_capacity=game_max_capacity_client,event_ticket_price=game_ticket_price_client,event_place=game_place_client,number_of_current_Fan=0,royaltyRate=royalty,SecondarySalesRules=SecondaryMR,SecondarySalesCapPrice=SecondaryMRN,category=category2,EventBanner=banner)
        event_created.save()

        return render(request, 'Club\eventcreation.html')
    return render(request, 'Club\eventcreation.html',{"categories":Category})




@login_required(login_url='/login/  ')
def myEvents(request):
    userEventsList=queryEvents('event_organizer',request.user.pk)[0]
    return render(request,'Club\ownedEvents.html',{"all_events":userEventsList})
    
    
counter=0


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
    return render(request,'Club\MyClub.html')


def getTokenOwners(request,TokenId):
    OwnersDataQuery=getOwners(TokenID=TokenId,ContractAddress="0x44872B49d25c1A3A22C432b3e42290dE9103e53b")
    OwnersHistory=[]
    Tr=0
    print(OwnersDataQuery)
    for owner in OwnersDataQuery['result']:
        OwnersHistory.append({'id':Tr,'timestamps':owner['block_timestamp'],'from':owner['from_address'],'to':owner['to_address'],'value':owner['value']})
        Tr+=1
    print(OwnersHistory)
    return render(request,"Club\OwnersTable.html",{"OwnersData":OwnersHistory})


def qr_ccode_scan_view(request):
    return render(request,"qr_code_scan.html")



from django.http import JsonResponse

def check_qr_code(request):
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        # Perform the comparison with values stored in the database
        # Retrieve relevant data and compare with qr_code
        db_query=QrCodeChecking.objects.all()
        flag=False
        tokenid=0
        for hash in db_query:
            if hash.hash == qr_code and hash.checked==False:
                flag=True
                tokenid=hash.token_id
                hash.checked=True
                hash.save()
                break
        # Example comparison
        if flag == True:
            
            query=EventsticketsMinted.objects.get(NFT_token_id=tokenid)
            query.checked=True
            query.save()
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})






#-------------- Analytics calculator -----------------------------------------



def Revenue_Calc(pk,query_object,query):
    current_date = datetime.now()
    print(current_date)
    current_month = current_date.month
    print("Current Month:", current_month)

    last_month = current_date.replace(day=1) - timedelta(days=1)
    last_month_number = last_month.month
    print("Last Month:", last_month_number)
    current_month_revenue=0
    last_month_revenue=250
    for game in query:
        if game.datebought.month == current_month:
            current_month_revenue+=game.event_id.event_ticket_price
        else:
            if game.event_date_time.month==last_month:
                last_month_revenue+=game.event_id.event_ticket_price
    alpha=((current_month_revenue - last_month_revenue) / last_month_revenue) * 100
    return (round(alpha,2),current_month_revenue)
        

def Royalty_Calc(request,userid):
    club_query=myClub.objects.get(pk=userid)
    wallet_address=club_query.RoyaltyReceiverAddresse
    balance=get_balance(wallet_address)
    return JsonResponse({'balance': balance})




def Volume_Traded_Calc(request,userid):
    query=EventsticketsMinted.objects.filter(**{"organizer_id":userid})
    volume=0
    for row in query:
        volume+=VolumneTraded(str(row.NFT_token_id))
    return JsonResponse({'volume': volume})




def AttendanceRateCalc(pk,query_object):
    AttendanceRate=0
    for event in query_object:
        AttendanceRate+=event.number_of_current_Fan / event.event_maximum_capacity
    return round(AttendanceRate * 100,2)


def LatestTransactions(pk,query):
    log={}
    res=[]
    for tickets_minted in query[0:4]:
        log['name']=tickets_minted.NFT_owner_account.username
        log['event_name']=str(tickets_minted.event_id.Team1Name)+" vs "+str(tickets_minted.event_id.Team2Name)
        log['token_id']=tickets_minted.NFT_token_id
        log['timestamp']=tickets_minted.TimeStamp
        res.append(log)
        log={}
    return res


def MostPopularGames(pk,query_object):
    from django.db.models import F, ExpressionWrapper, DecimalField

    query = query_object.annotate(
    revenue=ExpressionWrapper(F('event_ticket_price') * F('number_of_current_Fan'),
                              output_field=DecimalField())
).order_by('-revenue')[:5]
    log={}
    res=[]
    for game in query:
        log['img_url']=game.Team2Logo
        log['name']=str(game.Team1Name)+" vs "+str(game.Team2Name)
        log['total_revenue']=game.number_of_current_Fan * game.event_ticket_price
        log['date']=game.event_date_time.date
        res.append(log)
        log={}
    return res

def BestRevenueEvent(pk,queryEvents):
    mapping={}
    for event in queryEvents:
        mapping[event.pk]=event.event_ticket_price * event.number_of_current_Fan
    
    sorted_dict = dict(sorted(mapping.items(), key=lambda item: item[1], reverse=True))

    event_result=EventsCreated.objects.get(pk=next(iter(sorted_dict.items()))[0])

    return {"name":event_result.Team2Name,"date":event_result.event_date_time.date(),"revenue":next(iter(sorted_dict.items()))[1],"img":event_result.Team2Logo}

def TotalTicketSold(pk,queryEvents):
    number_of_tickets=0
    for event in queryEvents:
        number_of_tickets+=event.number_of_current_Fan
    return number_of_tickets




def RenderGames(pk,queryEvents):
    events=[]
    event={}
    for eve in queryEvents:
        event['name']=str(eve.Team1Name)+" vs "+str(eve.Team2Name)
        event['place']=eve.event_place
        event['date']=eve.event_date_time
        event['price']=eve.event_ticket_price
        event['status']=eve.number_of_current_Fan
        event['img']=eve.Team2Logo
        event['royalty']=eve.royaltyRate
        event['id']=eve.id
        events.append(event)
        event={}
    return events


def renderAnalytics(request):
    user_pk=request.user.pk
    query_object=EventsCreated.objects.filter(**{"event_organizer_id":user_pk})
    query=EventsticketsMinted.objects.filter(**{"organizer_id":user_pk})
    
    revenue=Revenue_Calc(user_pk,query_object,query)
    Rev_from_ticket=revenue[1]
    deltaRevenue=revenue[0]
    AttendanceRate=AttendanceRateCalc(user_pk,query_object)
    if deltaRevenue<0:
        indicator=0
    else:
        indicator=1
    latest_transactions_list=LatestTransactions(user_pk,query)
    ppopulargames=MostPopularGames(user_pk,query_object)
    Bestevent=BestRevenueEvent(user_pk,query_object)
    TotalTickets=TotalTicketSold(user_pk,query_object)
    AllGames=RenderGames(user_pk,query_object)
    return render(request,'Club\Dashboard.html',{"rev":Rev_from_ticket,"delta":deltaRevenue,"att":AttendanceRate,"ind":indicator,"pg":ppopulargames,"transaction":latest_transactions_list,"bestevent":Bestevent,"numberoftickets":TotalTickets,"games":AllGames,"user_id":user_pk})



def eventDashboard(request,eventId):
    queryTickets=EventsticketsMinted.objects.filter(**{"event_id":eventId})
    eventQuery=queryEvents("id",eventId)
    revenue=eventQuery[0][0]['price']*eventQuery[0][0]['currentNumber']
    currentnumber=eventQuery[0][0]['currentNumber']
    placesleft=eventQuery[0][0]['available_places']
    print(revenue)
    eventData=[]
    loyaltyQuery=loyalty(request.user.pk)
    print(request.user)
    print(loyaltyQuery)
    for ticket in queryTickets:
        if ticket.organizer==0:
            username=ticket.NFT_owner_address
            email='Not specified'
        username=ticket.NFT_owner_account.username
        email=ticket.NFT_owner_account.email
        eventData.append({"ownerName":username,"ownerAbrev":ticket.NFT_owner_account.username[0]+ticket.NFT_owner_account.username[-1],"ownerEmail":email,"Token_ID":ticket.NFT_token_id,"loyalty":loyaltyQuery[ticket.NFT_owner_account.username],"ownerID":ticket.NFT_owner_account.pk,"ticket_id":ticket.pk,"checkin":ticket.checked})
        print(eventData)
    return render(request,"Club\MyGame.html",{"eventData":eventData,"revenue":revenue,"cn":currentnumber,"pf":placesleft})