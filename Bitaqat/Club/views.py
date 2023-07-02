from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import F, Sum
from django.views.decorators.cache import cache_page
from .models import myClub, Event, MintedTickets, ClubsData
from Club.query import queryEvents
from Fan.utils import getOwners, VolumneTraded
from Fan.SmartContract import get_balance
from Fan.models import QrCodeChecking


@login_required(login_url='/login/')
def renderHomepage(request):
    """
    Render the homepage view for the authenticated user.
    """
    return render(request, 'Club/homepage.html')


@login_required(login_url='/login/')
def renderMarketplace(request):
    """
    Render the marketplace view for the authenticated user.
    """
    all_events = queryEvents()
    return render(request, 'Club/Marketplace.html', {'all_events': all_events})


@login_required(login_url='/login/')
def createEvents(request):
    """
    Create events view for the authenticated user.
    """
    current_user = request.user
    current_club = myClub.objects.get(pk=current_user)
    query_clubs = ClubsData.objects.all()
    clubs = []
    for club in query_clubs:
        if club.name != current_club.club.name:
            clubs.append(club.name)

    if request.method == 'POST':
        team2_name2 = request.POST.get('team')
        game_max_capacity_client = request.POST.get('maxnumber')
        game_ticket_price_client = request.POST.get('price')
        game_place_client = request.POST.get('city')
        royalty = request.POST.get('royap')
        banner = request.POST.get('banner')
        opposite_club = ClubsData.objects.get(name=team2_name2)
        event_created = Event(
            organizer=current_club,
            opposite_team=opposite_club,
            maximum_capacity=game_max_capacity_client,
            ticket_price=game_ticket_price_client,
            place=game_place_client,
            current_fan_count=0,
            royalty_rate=royalty,
            banner=banner
        )
        event_created.save()

        return render(request, 'Club/eventcreation.html')

    return render(request, 'Club/eventcreation.html', {"clubs": clubs})


@login_required(login_url='/login/')
def logoutUser(request):
    """
    Logout the user and redirect to the landing page.
    """
    logout(request)
    return HttpResponseRedirect(reverse("authentication:landingPage"))


@login_required(login_url='/login/')
def renderAttendedEvents(request, guestID, guestName):
    """
    Render the attended events view for the specified guest.
    """
    organizer = myClub.objects.get(pk=request.user)
    ticketsQuery = MintedTickets.objects.filter(
        owner_account=guestID, organizer=organizer.pk
    )
    return render(request, 'Club/AttandedEvents.html', {"attendedEvents": ticketsQuery, "guestName": guestName})


@login_required(login_url='/login/')
def getTokenOwners(request, tokenId):
    """
    Retrieve the token owners data for the specified tokenId.
    """
    OwnersDataQuery = getOwners(
        TokenID=tokenId, ContractAddress="0x44872B49d25c1A3A22C432b3e42290dE9103e53b"
    )
    OwnersHistory = []
    Tr = 0
    for owner in OwnersDataQuery['result']:
        OwnersHistory.append({
            'id': Tr,
            'timestamps': owner['block_timestamp'],
            'from': owner['from_address'],
            'to': owner['to_address'],
            'value': owner['value']
        })
        Tr += 1
    return render(request, "Club/OwnersTable.html", {"OwnersData": OwnersHistory})


"""
<-----------------------------QR CODE SCANNING LOGIC----------------------------->

"""


@login_required(login_url='/login/')
def qrCodeScanView(request):
    """
    Render the QR code scan view.
    """
    return render(request, "qr_code_scan.html")


@login_required(login_url='/login/')
def checkQRCode(request):
    """
    Check the scanned QR code and perform relevant actions.
    """
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        db_query = QrCodeChecking.objects.filter(hash=qr_code, checked=False)
        flag = False
        tokenid = 0
        for hash in db_query:
            flag = True
            tokenid = hash.token_id
            hash.checked = True
            hash.save()
            break

        if flag:
            query = MintedTickets.objects.get(token_id=tokenid)
            query.checked = True
            query.save()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False})


"""
<-----------------------------GAMES ANALYTICS LOGIC----------------------------->

"""


def calculateRevenue():
    """
    Calculate revenue and delta revenue for the specified queryObject.
    """
    # Get the current month's revenue
    current_month_revenue = Event.objects.filter(
        datetime__month=timezone.now().month
    ).aggregate(
        revenue=Sum(F('current_fan_count') * F('ticket_price'))
    )['revenue']

    # Get the previous month's revenue
    previous_month_revenue = Event.objects.filter(
        datetime__month=timezone.now().month - 1
    ).aggregate(
        revenue=Sum(F('current_fan_count') * F('ticket_price'))
    )['revenue']
    previous_month_revenue = 1

    alpha = ((current_month_revenue - previous_month_revenue) /
             previous_month_revenue) * 100
    return (round(alpha, 2), current_month_revenue)


def calculateRoyalty(request, userId):
    """
    Calculate the royalty balance for the specified userId.
    """
    club_query = myClub.objects.get(pk=userId)
    wallet_address = club_query.RoyaltyReceiverAddresse
    balance = get_balance(wallet_address)
    return JsonResponse({'balance': balance})


def calculateVolumeTraded(request, userId):
    """
    Calculate the volume traded for the specified userId.
    """
    query = MintedTickets.objects.filter(organizer_id=userId)
    volume = 0
    for row in query:
        volume += VolumneTraded(str(row.token_id))
    return JsonResponse({'volume': volume})


def calculateAttendanceRate(queryObject):
    """
    Calculate the attendance rate for the specified queryObject.
    """
    attendanceRate = 0
    for event in queryObject:
        attendanceRate += event["current_fan_count"] / \
            event["maximum_capacity"]
    return round(attendanceRate * 100, 2)


def getLatestTransactions(query):
    """
    Retrieve the latest transactions for the specified query.
    """
    ticket_data = {}
    tickets = []
    breaker = 0
    for ticket in query[len(query)-2:len(query)]:
        if breaker == 2:
            break
        try:
            ticket_data['username'] = ticket.owner_account.username
            ticket_data['name'] = ticket.event.opposite_team.name
            ticket_data['token_id'] = ticket.token_id
            tickets.append(ticket_data)
            breaker += 1
            ticket_data = {}
        except:
            pass

    return tickets


def getMostPopularGames(query):
    """
    Retrieve the most popular games based on revenue for the specified queryObject.
    """
    sorted_data = sorted(
        query, key=lambda x: x['current_fan_count'] * x['ticket_price'], reverse=True)
    return sorted_data[0:3]


def getBestRevenueEvent(queryEvents):
    """
    Retrieve the best revenue event based on ticket sales for the specified queryEvents.
    """
    result = queryEvents.annotate(
        product=F('ticket_price') * F('current_fan_count')).order_by('-product').first()

    return {
        "name": result.opposite_team.name,
        "date": result.datetime.date(),
        "revenue": result.ticket_price * result.current_fan_count,
        "img": result.opposite_team.logo
    }


def getTotalTicketsSold(queryEvents):
    """
    Calculate the total number of tickets sold for the specified queryEvents.
    """
    result = queryEvents.aggregate(total_sum=Sum('current_fan_count'))
    total_sum = result['total_sum']
    return total_sum


def renderGames(pk):
    """
    Render the games page for the specified queryEvents.
    """
    query = Event.objects.filter(organizer=pk)
    return query


@login_required(login_url='/login/')
def renderAnalytics(request):
    """
    Render the analytics dashboard page.
    """
    user_pk = request.user.pk
    NotLazyQuery = []
    query = {}
    queryObjectRevenue = Event.objects.filter(organizer=user_pk)
    organizer_name = queryObjectRevenue[0].organizer.club.name
    queryObjectsTickets = MintedTickets.objects.filter(organizer_id=user_pk)
    for obj in queryObjectRevenue:
        query['organizer'] = organizer_name
        query['datetime'] = obj.datetime
        query['place'] = obj.place
        query['maximum_capacity'] = obj.maximum_capacity
        query['ticket_price'] = obj.ticket_price
        query['current_fan_count'] = obj.current_fan_count
        query['royalty_rate'] = obj.royalty_rate
        query['opposite_team'] = {
            "name": obj.opposite_team.name, "logo": obj.opposite_team.logo.path}
        NotLazyQuery.append(query)
        query = {}
    revenue = calculateRevenue()
    rev_from_ticket = revenue[1]
    deltaRevenue = revenue[0]
    attendanceRate = calculateAttendanceRate(NotLazyQuery)

    if deltaRevenue < 0:
        indicator = 0
    else:
        indicator = 1
    latestTransactionsList = getLatestTransactions(queryObjectsTickets)
    popularGames = getMostPopularGames(NotLazyQuery)
    bestEvent = getBestRevenueEvent(queryObjectRevenue)
    totalTickets = getTotalTicketsSold(queryObjectRevenue)
    allGames = renderGames(user_pk)

    return render(request, 'Club\Dashboard.html', {
        "rev": rev_from_ticket,
        "delta": deltaRevenue,
        "att": attendanceRate,
        "ind": indicator,
        "pg": popularGames,
        "transaction": latestTransactionsList,  # 6
        "bestevent": bestEvent,
        "numberoftickets": totalTickets,
        "games": allGames,  # expensive (3-4 queries per game)
        "user_id": user_pk,
        "org": organizer_name
    })


@login_required(login_url='/login/')
def eventDashboard(request, eventId):
    """
    Render the event dashboard page for the specified eventId.
    """
    ticketsQuery = MintedTickets.objects.filter(event_id=eventId)

    eventQuery = queryEvents("id", eventId, history=True)

    eventData = []
    for ticket in ticketsQuery:
        if ticket.owner_account == None:
            username = ticket.owner_crypto_address
            email = 'Not specified'
            ownerID = None
        else:
            username = ticket.owner_account.username
            email = ticket.owner_account.email
            ownerID = ticket.owner_account.pk

        eventData.append({
            "ownerName": username,
            "ownerEmail": email,
            "Token_ID": ticket.token_id,
            "ownerID": ownerID
        })
    return render(request, "Club\MyGame.html", {
        "eventData": eventData,
        "Data": eventQuery
    })
