import io
import requests
import random
import qrcode
import hashlib
import time
from threading import Timer
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .SmartContract import main, upload_to_ipfs
from Club.query import queryEvents
from Club.models import Event, MintedTickets
from Fan.models import QrCodeChecking, myFan
from authentication.models import myUsers
from django.views.decorators.cache import cache_page
from django.core.cache import cache


@login_required(login_url='/login/')
def renderHomepage(request):
    """
    Renders the homepage view for an authenticated user.
    """
    return render(request, 'Fan\homepage.html')


@login_required(login_url='/login/')
@cache_page(60 * 2)
def renderMarketplace(request):
    """
    Renders the marketplace view for an authenticated user and retrieves all available events.
    """
    all_events = queryEvents()
    return render(request, 'Fan\Marketplace.html', {'all_events': all_events})


def match_address_with_account(ownedPublicAddress):
    """
    Searches the database to find the user account associated with the provided address.
    """
    queriedGuest = myFan.objects.get(public_key=ownedPublicAddress)
    user = myUsers.objects.get(pk=queriedGuest.user_id)
    return user


@login_required(login_url='/login/')
def buyTicket(request, event_id):
    """
    Handles the purchase of a ticket for a specific event.
    """
    if request.method == "POST":
        user_db = myFan.objects.get(pk=request.user.pk)
        query = Event.objects.get(pk=event_id)
        buyer_crypto_address = user_db.public_key
        tokenuri = upload_to_ipfs(str(query.organizer.club.name)+" vs "+str(query.opposite_team.name)+" #"+str(query.current_fan_count), "This is a match between " +
                                  str(query.organizer.club.name) + " and "+str(query.opposite_team.name)+" it will be played at "+str(query.place)+" on "+str(query.datetime.date())+" at "+str(query.datetime.time()), query.organizer.club.logo.path)
        response = requests.get(tokenuri)
        if response.status_code == 200:
            token_id = main(buyer_crypto_address, query.royalty_rate*1000,
                            "0x074C6794461525243043377094DbA36eed0A951B", tokenuri)

        query.current_fan_count += 1
        query.save()
        ticket_query_to_db = MintedTickets(event_id=query.id, owner_crypto_address=str(buyer_crypto_address), owner_account=match_address_with_account(
            buyer_crypto_address), token_id=token_id, organizer=query.organizer)
        ticket_query_to_db.save()
        return JsonResponse({"status": "success"})

    return HttpResponseRedirect(reverse('Fan:renderMarketplace'))


@login_required(login_url='/login/')
@cache_page(120)
def renderInventory(request):
    """
    Renders the inventory view for an authenticated user and retrieves their ticket collection.
    """

    cache_key = request.user.pk
    inventory = cache.get(cache_key)
    if inventory is None:
        events = []
        event_data = {}
        inventory = []
        collection = MintedTickets.objects.filter(
            owner_account=request.user.pk)
        for tix in collection:
            event_id = tix.event.pk
            if event_id in events:
                inventory.append(
                    {"date": event_data[str(event_id)], "token": tix.token_id, "checked": tix.checked})
            else:
                event_data[str(event_id)] = {"logo1": tix.organizer.club.logo, "name1": tix.organizer.club.name, "logo2": tix.event.opposite_team.logo,
                                             "name2": tix.event.opposite_team.name, "date": tix.event.datetime, "place": tix.event.place}
                inventory.append(
                    {"date": event_data[str(event_id)], "token": tix.token_id, "checked": tix.checked})

        cache.set(cache_key, inventory)
    return render(request, 'Fan\Inventory.html', {'collection': inventory})


@login_required(login_url='/login/')
def renderKeys(request):
    """
    Renders the keys view for an authenticated user and retrieves their public and private keys.
    """
    user = request.user
    query_object = myFan.objects.get(pk=user)
    public_key = query_object.public_key
    private_key = query_object.private_key
    return render(request, "Fan\Keys.html", {"pk": private_key, "publickey": public_key})


def hashData(receiver_address, token_id):
    """
    Hashes the provided data (receiver address, token ID, and current timestamp) using a shuffled order of characters.
    """
    input_data = receiver_address + str(token_id) + str(time.time())
    input_data = list(input_data)
    random.shuffle(input_data)
    shuffled_data = ''.join(input_data)
    hashed_data = hashlib.sha256(shuffled_data.encode()).hexdigest()
    return hashed_data


def generate_qr_code_hash(hashed_data):
    """
    Generates a QR code image from the provided hashed data.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(hashed_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    qr_image.save(buffer, format="PNG")
    image_file = ContentFile(buffer.getvalue())
    return image_file


@login_required(login_url='/login/')
def generate_qr_code(request, token_id):
    """
    Generates a QR code for the provided token ID and saves it in the database.
    """
    user = request.user
    query_object = myFan.objects.get(pk=user)
    public_key = query_object.public_key
    qr_code_hash = hashData(public_key, token_id)
    qr_code_img = generate_qr_code_hash(qr_code_hash)
    qr_code = QrCodeChecking(Qrcode="", hash=qr_code_hash, token_id=token_id)
    qr_code.Qrcode.save(str(qr_code.token_id)+"Qrcode.png",
                        qr_code_img, save=True)
    qr_code.save()
    timer = Timer(180, verify_qr_code, args=(token_id,))
    timer.start()
    return render(request, 'Fan/Qrcode.html', {"image": qr_code.Qrcode})


def verify_qr_code(token_id):
    """
    Verifies the QR code identified by the provided token ID.
    """
    try:
        qr_code = QrCodeChecking.objects.get(token_id=token_id)
    except QrCodeChecking.DoesNotExist:
        return  # QR code record not found, handle accordingly

    if qr_code.checked:
        return  # QR code already verified, handle accordingly

    qr_code.delete()
