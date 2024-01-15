from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import F, Sum
from .models import myClub, Events, MintedTickets
from Fan.utils import getOwners, VolumneTraded
from Fan.SmartContract import get_balance
from Fan.models import CryptoWallets, QrCodeChecking

@login_required(login_url='/login/')
def renderHomepage(request):
    """
    Render the homepage view for the authenticated user.
    """
    return render(request, 'Club/HOME.html')


@login_required(login_url='/login/')
def renderMarketplace(request):
    """
    Render the marketplace view for the authenticated user.
    """
    current_datetime = timezone.now()
    all_events = Events.objects.select_related(
        'team1').select_related('team2').filter(datetime__gt=current_datetime)
    return render(request, 'Club/GAMES.html', {'all_events': all_events})


@login_required(login_url='/login/')
def createEvents(request):
    """
   Create events based on inputs and save it in the database
    """
    current_user = request.user
    current_club = myClub.objects.get(pk=current_user)
    clubs = myClub.objects.exclude(pk=current_user)
    if request.method == 'POST':
        team2_name2 = request.POST.get('team')
        game_max_capacity_client = request.POST.get('maxnumber')
        game_ticket_price_client = request.POST.get('price')
        game_place_client = request.POST.get('city')
        royalty = request.POST.get('royap')
        datetime = request.POST.get('date')
        banner = request.FILES['banner']
        maximum_ticket_per_account = request.POST.get('maxnumberticket')
        opposite_club = myClub.objects.get(name=team2_name2)
        event_created = Events(
            team1=current_club,
            team2=opposite_club,
            capacity=game_max_capacity_client,
            price=game_ticket_price_client,
            place=game_place_client,
            current_fan_count=0,
            royalty_rate=royalty,
            banner=banner,
            datetime=datetime,
            maximum_ticket_per_account=maximum_ticket_per_account
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
    Return all the events watched by the user for the current club
    """

    ticketsQuery = MintedTickets.objects.select_related(
        'event__team1', 'event__team2'
    ).filter(username=guestID)
    return render(request, 'Club/AttandedEvents.html', {"collection": ticketsQuery, "guestName": guestName})


@login_required(login_url='/login/')
def getTokenOwners(request, tokenId):
    """
    Retrieve the owner history of a certain NFT using its token id
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
    Render the QR code scan page.
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


def calculateRevenue( query):
    """
   Calculate current month revenue.
    """
    # Get the current month's revenue
    timezone_now = timezone.now().month
    queryObjectRevenue = query
    current_month_revenue = 0
    totalrevenue = 0
    for event in queryObjectRevenue:
        if event.datetime.month == timezone_now:
            current_month_revenue += event.current_fan_count * event.price
        totalrevenue = event.current_fan_count * event.price

    return (current_month_revenue, totalrevenue)


def calculateRoyalty(request, userId):
    """
    Return money earned from royalties by checking the balance of the club's royalty wallet
    """
    wallet_address = CryptoWallets.objects.get(username=userId)
    balance = get_balance(wallet_address)
    return JsonResponse({'balance': balance})


def calculateVolumeTraded(request, userId):
    """
    Calculate the volume traded for all the NFT issued by the club .
    """
    query = MintedTickets.objects.select_related(
        "username").filter(username=userId)
    volume = 0
    for row in query:
        volume += VolumneTraded(str(row.token_id))
    return JsonResponse({'volume': volume})


def calculateAttendanceRate(queryObject):
    """
    Calculate the attendance rate of the club.
    """
    attendanceRate = 0
    counter = 0
    for event in queryObject:
        attendanceRate += event.current_fan_count / \
            event.capacity
        counter += 1
    return round(attendanceRate/counter * 100, 2)


def getMostPopularGames(query):
    """
    Retrieve the most popular games based on revenue.
    """
    sorted_data = sorted(
        query, key=lambda x: x.current_fan_count * x.price, reverse=True)
    return sorted_data[0:3]


def getBestRevenueEvent(queryEvents):
    """
    Retrieve the most sold out event.
    """
    result = queryEvents.annotate(
        product=F('price') * F('current_fan_count')).order_by('-product').first()
    if result != None:
        return {
            "name": result.team2.name,
            "date": result.datetime.date(),
            "revenue": result.price * result.current_fan_count,
            "img": result.team2.logo
        }
    return None


def getTotalTicketsSold(queryEvents):
    """
    Calculate the total number of tickets sold for the club.
    """
    result = queryEvents.aggregate(total_sum=Sum('current_fan_count'))
    total_sum = result['total_sum']
    return total_sum


@login_required(login_url='/login/')
def renderAnalytics(request):
    """
    Combine all previous functions and transfer them to the HTML page
    """
    attendanceRate = 0
    counter = 0
    current_month_revenue = 0
    totalrevenue = 0

    timezone_now = timezone.now().month

    user_pk = request.user.pk
    

    queryEvents = Events.objects.select_related(
        'team1').select_related('team2').filter(team1=user_pk)

    if queryEvents != []:
        print(len(queryEvents))
        organizer_name = queryEvents[0].team1.name

    queryObjectsTickets = MintedTickets.objects.select_related(
        'event__organizer__club', 'event__opposite_team'
    ).filter(organizer_id=user_pk)

    # Calculate revenue
    for event in queryEvents:
        if event.datetime.month == timezone_now:
            current_month_revenue += event.current_fan_count * event.price
        totalrevenue += event.current_fan_count * event.price

    rev_from_ticket = current_month_revenue
    # end of Revenue calculations

    # Calculate attendance rate
    for event in queryEvents:
        attendanceRate += event.current_fan_count / \
            event.capacity
        counter += 1
    attendanceRate = round(attendanceRate/counter * 100, 2)
    # end of attendancy rate calculations

    popularGames = getMostPopularGames(queryEvents)
    bestEvent = getBestRevenueEvent(queryEvents)
    totalTickets = getTotalTicketsSold(queryEvents)
    allGames = queryEvents

    return render(request, 'Club/Dashboard.html', {
        "rev": rev_from_ticket,
        "att": attendanceRate,
        "pg": popularGames,  
        "bestevent": bestEvent,
        "numberoftickets": totalTickets,
        "games": allGames, 
        "user_id": user_pk,
        "org": organizer_name,
        "totalrevenue": totalrevenue
    })



@login_required(login_url='/login/')
def eventDashboard(request, eventId):
    """
    Return a dashboard with data for a certain event.
    """
    ticketsQuery = MintedTickets.objects.select_related(
        'event__team1'
    ).filter(event=eventId)

    eventQuery = Events.objects.select_related(
        'team1').select_related('team2').filter(id=eventId
                                                                  )
    Nof = 0
    for info in eventQuery:
        Nof = info.capacity-info.current_fan_count

    eventData = []
    for ticket in ticketsQuery:
        if ticket.username == None:
            username = ticket.newOwner
            email = 'Not specified'
            ownerID = None
        else:
            username = ticket.username
            email = ticket.username.email
            ownerID = ticket.username.pk

        eventData.append({
            "ownerName": username,
            "ownerEmail": email,
            "Token_ID": ticket.token_id,
            "ownerID": ownerID,
            "checkin": ticket.checked
        })

    return render(request, "Club/MyGame.html", {
        "eventData": eventData,
        "Data": eventQuery,
        "nof": Nof
    })
