import io
from Fan.models import QrCodeChecking
from django.core.files.base import ContentFile
from threading import Timer
from datetime import datetime, timedelta
import qrcode
import hashlib
import random
from django.shortcuts import render
import datetime
from Club.models import Event
from Club.models import MintedTickets
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import myUsers
from Fan.models import myFan, loyalFan
import time
from .utils import fetchNftsMetadata
import asyncio
from django.http import HttpResponseRedirect, JsonResponse
from Club.query import queryEvents, queryAttEvents
from django.urls import reverse
from .SmartContract import main, upload_to_ipfs
from django.http import HttpResponse
from PIL import Image


@login_required(login_url='/login/  ')
def renderHomepage(request):
    print(request.user)
    eventNumber = queryEvents()[1]
    attandeesNumber = len(myFan.objects.all().filter())
    ticketsNumber = len(MintedTickets.objects.all().filter())
    return render(request, 'Fan\homepage.html', {"user_name": request.user.username, "eventNumber": eventNumber, "attandeesNumber": attandeesNumber, 'ticketsNumber': ticketsNumber})


@login_required(login_url='/login/  ')
def renderMarketplace(request):
    all_events = queryEvents()[0]
    return render(request, 'Fan\Marketplace.html', {'all_events': all_events})


@login_required(login_url='/login/  ')
def renderSpecificEventPage(request, event_id):
    # GETTING EVENTS DATA FROM DATABASE
    event = queryEvents("pk", event_id)
    print(event[0][0])
    return render(request, 'Fan\event_info_page.html', {'all_events': event[0][0]})


# Search in the database who owns this address
def match_address_with_account(ownedPublicAddress):
    queriedGuest = myFan.objects.get(public_crypto_address=ownedPublicAddress)
    user = myUsers.objects.get(pk=queriedGuest.user_id)
    return user


def buyTicket(request, event_id):
    if request.method == "POST":
        user_db = myFan.objects.get(pk=request.user.pk)
        query = Event.objects.get(pk=event_id)
        buyer_crypto_address = user_db.public_crypto_address
        print(buyer_crypto_address)
        tokenuri = upload_to_ipfs(str(query.team1_name)+" vs "+str(query.team2_name)+" #"+str(query.current_fan_count), "This is a match between " +
                                  str(query.team1_name) + " and "+str(query.team2_name)+" it will be played at "+str(query.place)+" on "+str(query.datetime.date())+" at "+str(query.datetime.time()), query.team1_logo.path)
        # calling the minting function
        time.sleep(3)
        token_id = main(buyer_crypto_address, query.royalty_rate*1000,
                        "0x074C6794461525243043377094DbA36eed0A951B", tokenuri)
        query.current_fan_count += 1
        query.save()
        ticket_query_to_db = MintedTickets(event_id=query, owner_crypto_address=str(buyer_crypto_address), owner_account=match_address_with_account(
            buyer_crypto_address), token_id=token_id, organizer=query.organizer, datebought="2023-06-19")
        ticket_query_to_db.save()

        loyaltyQuery = loyalFan.objects.filter(
            **{'organizer': query.organizer, "guest": request.user.pk})
        if len(loyaltyQuery) != 0:
            loyaltyQuery[0].eventsCount += 1
            loyaltyQuery[0].save()
        else:
            loyalty = loyalFan(guest=request.user,
                               organizer=query.organizer, eventsCount=1)
            loyalty.save()
        return JsonResponse({"status": "success"})

    return HttpResponseRedirect(reverse('Fan:renderMarketplace'))


# def requestMetadata(name,description,image_url):
#     return {"name":name,}


def renderInventory(request):
    attendee = myFan.objects.get(user_id=request.user.pk)
    userAddress = attendee.public_crypto_address
    collection = fetchNftsMetadata(userAddress)
    all_events = []
    event = {}
    for events in collection:
        object = MintedTickets.objects.get(
            token_id=events['tokenid'])
        event['team1_logo'] = object.event_id.team1_logo
        event['team2_logo'] = object.event_id.team2_logo
        event['team1_name'] = object.event_id.team1_name
        event['team2_name'] = object.event_id.team2_name
        event['date'] = object.event_id.datetime
        event['tokenid'] = object.token_id
        if object.checked == True:
            event['checked'] = True
        else:
            event['checked'] = False
        all_events.append(event)
        event = {}
    return render(request, 'Fan\Inventory.html', {"collection": all_events})


def ReturnImg(request):
    object = Event.objects.get(pk=2)
    response = HttpResponse(content_type="image/jpeg")
    image = object.team1_logo
    # Set the image content as the response content
    response.write(image)

    return response


def renderKeys(request):
    user2 = request.user
    query_object = myFan.objects.get(pk=user2)
    public_key = query_object.public_crypto_address
    private_key = query_object.private_crypto_address
    return render(request, "Fan\Keys.html", {"pk": private_key, "publickey": public_key})


def hashData(receiver_address, token_id):
    input_data = receiver_address + str(token_id) + str(time.time())
    # Convert the input string to a list of characters
    input_data = list(input_data)
    random.shuffle(input_data)  # Shuffle the characters randomly
    # Convert the shuffled characters back to a string
    shuffled_data = ''.join(input_data)

    hashed_data = hashlib.sha256(shuffled_data.encode()).hexdigest()
    return hashed_data


def generate_qr_code_hash(hashed_data):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(hashed_data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    # Convert the image to PNG format
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    image_file = ContentFile(buffer.getvalue())

    # Create a new QrCodeChecking instance and assign the image file

    return image_file


def generate_qr_code(request, token_id):
    # Handle the button click event
    # Generate the QR code hash
    user2 = request.user
    query_object = myFan.objects.get(pk=user2)
    public_key = query_object.public_crypto_address
    qr_code_hash = hashData(public_key, token_id)
    qr_code_img = generate_qr_code_hash(qr_code_hash)
    # Save the QR code hash and token ID in the database

    qr_code = QrCodeChecking(Qrcode="", hash=qr_code_hash, token_id=token_id)
    qr_code.Qrcode.save(str(qr_code.token_id)+"Qrcode.png",
                        qr_code_img, save=True)
    qr_code.save()

    # Start a background timer for 2 minutes
    timer = Timer(180, verify_qr_code, args=(token_id,))
    timer.start()

    return render(request, 'Fan/Qrcode.html', {"image": qr_code.Qrcode})


def verify_qr_code(token_id):
    try:
        qr_code = QrCodeChecking.objects.get(token_id=token_id)
    except QrCodeChecking.DoesNotExist:
        return  # QR code record not found, handle accordingly

    if qr_code.checked:
        return  # QR code already verified, handle accordingly

    qr_code.delete()
