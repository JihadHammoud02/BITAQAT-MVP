from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from authentication.models import myUsers
from .models import myClub, Event, MintedTickets
from django.urls import reverse
from django.http import HttpResponseRedirect
from Club.query import queryEvents, countAttandees, loyalty, queryAttEvents
from Fan.models import myFan
import datetime
from Fan.utils import getOwners, VolumneTraded
import time
from Fan.SmartContract import get_balance
from datetime import datetime, timedelta
from Fan.models import QrCodeChecking
# A decorator that checks if the user is logged in. If not, it redirects to the login page.


@login_required(login_url='/login/  ')
def renderHomepage(request):
    return render(request, 'Club\homepage.html')


@login_required(login_url='/login/  ')
def renderMarketplace(request):
    all_events = queryEvents()[0]
    return render(request, 'Club\Marketplace.html', {'all_events': all_events})


@login_required(login_url='/login/  ')
def createEvents(request):
    if request.method == 'POST':
        team1_name1 = request.POST.get('name1')
        team2_name2 = request.POST.get('name2')
        team1_logo1 = request.FILES['logo1']
        team2_logo2 = request.FILES['logo2']
        game_date_client = request.POST.get('eventdate')
        game_max_capacity_client = request.POST.get('maxnumber')
        game_ticket_price_client = request.POST.get('price')
        game_place_client = request.POST.get('city')
        royalty = request.POST.get('royap')
        banner = request.POST.get('banner')

        event_created = Event(organizer=request.user, team1_name=team1_name1, team2_name=team2_name2, team1_logo=team1_logo1, team2_logo=team2_logo2, datetime=game_date_client, maximum_capacity=game_max_capacity_client,
                              ticket_price=game_ticket_price_client, place=game_place_client, current_fan_count=0, royalty_rate=royalty,  banner=banner)
        event_created.save()

        return render(request, 'Club\eventcreation.html')
    return render(request, 'Club\eventcreation.html')


@login_required(login_url='/login/  ')
def myEvents(request):
    userEventsList = queryEvents('organizer', request.user.pk)[0]
    return render(request, 'Club\ownedEvents.html', {"all_events": userEventsList})


counter = 0


# logout the User
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse("authentication:landingPage"))


def renderAttandedEvents(request, guestID, guestName):
    AttandedEvents = queryAttEvents(guestID, request.user)
    print(AttandedEvents)
    return render(request, 'Club\AttandedEvents.html', {"attandedEvents": AttandedEvents, "guestName": guestName})


def checkInGuest(request, mintedID_DB):
    mintedTicketQuery = MintedTickets.objects.get(pk=mintedID_DB)
    mintedTicketQuery.checkIn_Time = datetime.datetime.now()
    mintedTicketQuery.save()
    return HttpResponseRedirect(reverse("Club:eventDashboard", args=(mintedTicketQuery.event_id.pk,)))


def getClubData(request):
    return render(request, 'Club\MyClub.html')


def getTokenOwners(request, TokenId):
    OwnersDataQuery = getOwners(
        TokenID=TokenId, ContractAddress="0x44872B49d25c1A3A22C432b3e42290dE9103e53b")
    OwnersHistory = []
    Tr = 0
    print(OwnersDataQuery)
    for owner in OwnersDataQuery['result']:
        OwnersHistory.append({'id': Tr, 'timestamps': owner['block_timestamp'],
                             'from': owner['from_address'], 'to': owner['to_address'], 'value': owner['value']})
        Tr += 1
    print(OwnersHistory)
    return render(request, "Club\OwnersTable.html", {"OwnersData": OwnersHistory})


def qr_ccode_scan_view(request):
    return render(request, "qr_code_scan.html")


def check_qr_code(request):
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        # Perform the comparison with values stored in the database
        # Retrieve relevant data and compare with qr_code
        db_query = QrCodeChecking.objects.all()
        flag = False
        tokenid = 0
        for hash in db_query:
            if hash.hash == qr_code and hash.checked == False:
                flag = True
                tokenid = hash.token_id
                hash.checked = True
                hash.save()
                break
        # Example comparison
        if flag == True:

            query = MintedTickets.objects.get(token_id=tokenid)
            query.checked = True
            query.save()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False})


# -------------- Analytics calculator -----------------------------------------


def Revenue_Calc(pk, query_object, query):
    current_date = datetime.now()
    print(current_date)
    current_month = current_date.month
    print("Current Month:", current_month)

    last_month = current_date.replace(day=1) - timedelta(days=1)
    last_month_number = last_month.month
    print("Last Month:", last_month_number)
    current_month_revenue = 0
    last_month_revenue = 250
    for game in query:
        if game.datebought.month == current_month:
            current_month_revenue += game.event_id.ticket_price
        else:
            if game.datetime.month == last_month:
                last_month_revenue += game.event_id.ticket_price
    alpha = ((current_month_revenue - last_month_revenue) /
             last_month_revenue) * 100
    return (round(alpha, 2), current_month_revenue)


def Royalty_Calc(request, userid):
    club_query = myClub.objects.get(pk=userid)
    wallet_address = club_query.RoyaltyReceiverAddresse
    balance = get_balance(wallet_address)
    return JsonResponse({'balance': balance})


def Volume_Traded_Calc(request, userid):
    query = MintedTickets.objects.filter(**{"organizer_id": userid})
    volume = 0
    for row in query:
        volume += VolumneTraded(str(row.token_id))
    return JsonResponse({'volume': volume})


def AttendanceRateCalc(pk, query_object):
    AttendanceRate = 0
    for event in query_object:
        AttendanceRate += event.current_fan_count / event.maximum_capacity
    return round(AttendanceRate * 100, 2)


def LatestTransactions(pk, query):
    log = {}
    res = []
    for tickets_minted in query[0:4]:
        log['name'] = tickets_minted.owner_account.username
        log['event_name'] = str(
            tickets_minted.event_id.team1_name)+" vs "+str(tickets_minted.event_id.team2_name)
        log['token_id'] = tickets_minted.token_id
        log['timestamp'] = tickets_minted.TimeStamp
        res.append(log)
        log = {}
    return res


def MostPopularGames(pk, query_object):
    from django.db.models import F, ExpressionWrapper, DecimalField

    query = query_object.annotate(
        revenue=ExpressionWrapper(F('ticket_price') * F('current_fan_count'),
                                  output_field=DecimalField())
    ).order_by('-revenue')[:5]
    log = {}
    res = []
    for game in query:
        log['img_url'] = game.team2_logo
        log['name'] = str(game.team1_name)+" vs "+str(game.team2_name)
        log['total_revenue'] = game.current_fan_count * \
            game.ticket_price
        log['date'] = game.datetime.date
        res.append(log)
        log = {}
    return res


def BestRevenueEvent(pk, queryEvents):
    mapping = {}
    for event in queryEvents:
        mapping[event.pk] = event.ticket_price * \
            event.current_fan_count

    sorted_dict = dict(
        sorted(mapping.items(), key=lambda item: item[1], reverse=True))

    event_result = Event.objects.get(
        pk=next(iter(sorted_dict.items()))[0])

    return {"name": event_result.team2_name, "date": event_result.datetime.date(), "revenue": next(iter(sorted_dict.items()))[1], "img": event_result.team2_logo}


def TotalTicketSold(pk, queryEvents):
    number_of_tickets = 0
    for event in queryEvents:
        number_of_tickets += event.current_fan_count
    return number_of_tickets


def RenderGames(pk, queryEvents):
    events = []
    event = {}
    for eve in queryEvents:
        event['name'] = str(eve.team1_name)+" vs "+str(eve.team2_name)
        event['place'] = eve.place
        event['date'] = eve.datetime
        event['price'] = eve.ticket_price
        event['status'] = eve.current_fan_count
        event['img'] = eve.team2_logo
        event['royalty'] = eve.royalty_rate
        event['id'] = eve.id
        events.append(event)
        event = {}
    return events


def renderAnalytics(request):
    user_pk = request.user.pk
    query_object = Event.objects.filter(
        **{"organizer_id": user_pk})
    query = MintedTickets.objects.filter(**{"organizer_id": user_pk})

    revenue = Revenue_Calc(user_pk, query_object, query)
    Rev_from_ticket = revenue[1]
    deltaRevenue = revenue[0]
    AttendanceRate = AttendanceRateCalc(user_pk, query_object)
    if deltaRevenue < 0:
        indicator = 0
    else:
        indicator = 1
    latest_transactions_list = LatestTransactions(user_pk, query)
    ppopulargames = MostPopularGames(user_pk, query_object)
    Bestevent = BestRevenueEvent(user_pk, query_object)
    TotalTickets = TotalTicketSold(user_pk, query_object)
    AllGames = RenderGames(user_pk, query_object)
    return render(request, 'Club\Dashboard.html', {"rev": Rev_from_ticket, "delta": deltaRevenue, "att": AttendanceRate, "ind": indicator, "pg": ppopulargames, "transaction": latest_transactions_list, "bestevent": Bestevent, "numberoftickets": TotalTickets, "games": AllGames, "user_id": user_pk})


def eventDashboard(request, eventId):
    queryTickets = MintedTickets.objects.filter(**{"event_id": eventId})
    eventQuery = queryEvents("id", eventId)
    revenue = eventQuery[0][0]['price']*eventQuery[0][0]['currentNumber']
    currentnumber = eventQuery[0][0]['currentNumber']
    placesleft = eventQuery[0][0]['available_places']
    print(revenue)
    eventData = []
    loyaltyQuery = loyalty(request.user.pk)
    print(request.user)
    print(loyaltyQuery)
    for ticket in queryTickets:
        if ticket.organizer == 0:
            username = ticket.owner_crypto_address
            email = 'Not specified'
        username = ticket.owner_account.username
        email = ticket.owner_account.email
        eventData.append({"ownerName": username, "ownerAbrev": ticket.owner_account.username[0]+ticket.owner_account.username[-1], "ownerEmail": email, "Token_ID": ticket.token_id,
                         "loyalty": loyaltyQuery[ticket.owner_account.username], "ownerID": ticket.owner_account.pk, "ticket_id": ticket.pk, "checkin": ticket.checked})
        print(eventData)
    return render(request, "Club\MyGame.html", {"eventData": eventData, "revenue": revenue, "cn": currentnumber, "pf": placesleft})
