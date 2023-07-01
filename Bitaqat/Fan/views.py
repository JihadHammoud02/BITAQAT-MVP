import io

import requests
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
from Fan.models import myFan
import time
from .utils import fetchNftsMetadata
import asyncio
from django.http import HttpResponseRedirect, JsonResponse
from Club.query import queryEvents, queryAttEvents
from django.urls import reverse
from .SmartContract import main, upload_to_ipfs
from django.http import HttpResponse
from PIL import Image
from django.core.serializers import serialize
from Club.models import myClub


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
    return render(request, 'Fan\event_info_page.html', {'all_events': event[0][0]})


# Search in the database who owns this address
def match_address_with_account(ownedPublicAddress):
    queriedGuest = myFan.objects.get(public_key=ownedPublicAddress)
    user = myUsers.objects.get(pk=queriedGuest.user_id)
    return user


def buyTicket(request, event_id):
    if request.method == "POST":
        user_db = myFan.objects.get(pk=request.user.pk)
        query = Event.objects.get(pk=event_id)
        buyer_crypto_address = user_db.public_key
        print(buyer_crypto_address)
        tokenuri = upload_to_ipfs(str(query.organizer.club.name)+" vs "+str(query.opposite_team.name)+" #"+str(query.current_fan_count), "This is a match between " +
                                  str(query.organizer.club.name) + " and "+str(query.opposite_team.name)+" it will be played at "+str(query.place)+" on "+str(query.datetime.date())+" at "+str(query.datetime.time()), query.organizer.club.logo.path)
        # calling the minting function
        response = requests.get(tokenuri)
        print("resp: "+str(response))
        if response.status_code == 200:
            # calling the minting function
            token_id = main(buyer_crypto_address, query.royalty_rate*1000,
                            "0x074C6794461525243043377094DbA36eed0A951B", tokenuri)

        query.current_fan_count += 1
        query.save()
        ticket_query_to_db = MintedTickets(event_id=query.id, owner_crypto_address=str(buyer_crypto_address), owner_account=match_address_with_account(
            buyer_crypto_address), token_id=token_id, organizer=query.organizer)
        ticket_query_to_db.save()
        return JsonResponse({"status": "success"})

    return HttpResponseRedirect(reverse('Fan:renderMarketplace'))


def renderInventory(request):
    all_events = []
    event = {}
    collection = MintedTickets.objects.filter(
        **{"owner_account": request.user.pk})
    for eve in collection:
        event['team1_logo'] = eve.organizer.club.logo
        event['team2_logo'] = eve.event.opposite_team.logo
        event['team1_name'] = eve.organizer.club.name
        event['team2_name'] = eve.event.opposite_team.name
        event['date'] = eve.event.datetime
        event['tokenid'] = eve.token_id
        event['checked'] = eve.checked
        all_events.append(event)
        event = {}
    context = {'collection': all_events}
    return render(request, 'Fan\Inventory.html', context)


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
    public_key = query_object.public_key
    private_key = query_object.private_key
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
    public_key = query_object.public_key
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
