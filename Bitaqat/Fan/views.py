from Club.models import MintedTickets
from Fan.SmartContract import mainQrcode
import json
from django.views.decorators.csrf import csrf_exempt
import io
import requests
import random
import qrcode
import hashlib
import time
from threading import Timer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .SmartContract import main, upload_to_ipfs
from Club.models import Event, MintedTickets
from Fan.models import QrCodeChecking, myFan
from authentication.models import myUsers
from django.utils import timezone
from Fan.SmartContract import sendFromMother


@login_required(login_url='/login/')
def renderHomepage(request):
    """
    Renders the homepage view for an authenticated user.
    """
    return render(request, 'Fan\HOME.html')


@login_required(login_url='/login/')
def renderMarketplace(request):
    """
    Renders the marketplace view for an authenticated user and retrieves all available events.
    """
    current_datetime = timezone.now()
    all_events = Event.objects.select_related('organizer__club').select_related(
        'opposite_team').filter(datetime__gt=current_datetime)
    return render(request, 'Fan\GAMES.html', {'all_events': all_events})


def match_address_with_account(ownedPublicAddress):
    """
    Searches the database to find the user account associated with the provided address.
    """
    queriedGuest = myFan.objects.get(public_key=ownedPublicAddress)
    user = myUsers.objects.get(pk=queriedGuest.user_id)
    return user


def count_tickets_in_accounts(pk, event_id):
    query = MintedTickets.objects.filter(
        **{"event": event_id, "owner_account": pk})
    return len(query)


@login_required(login_url='/login/')
def buyTicket(request, event_id):
    """
    Handles the purchase of a ticket for a specific event.
    """
    if request.method == "POST":
        user_db = myFan.objects.select_related('user').get(pk=request.user.pk)
        query = Event.objects.select_related(
            'organizer__club').select_related('opposite_team').get(pk=event_id)
        if query.current_fan_count < query.maximum_capacity:
            if count_tickets_in_accounts(request.user.pk, event_id) < query.maximum_ticket_per_account:
                buyer_crypto_address = user_db.public_key
                try:
                    if not user_db.has_received_matic:
                        sendFromMother(buyer_crypto_address, 0.2)
                        user_db.has_received_matic = True
                        user_db.save()
                    tokenuri = upload_to_ipfs(str(query.organizer.club.name)+" vs "+str(query.opposite_team.name)+" #"+str(query.current_fan_count), "This is a match between " +
                                              str(query.organizer.club.name) + " and "+str(query.opposite_team.name)+" it will be played at "+str(query.place)+" on "+str(query.datetime.date())+" at "+str(query.datetime.time()), query.banner.path)

                    response = requests.get(tokenuri)
                    if response.status_code == 200:
                        activate_buying = main(buyer_crypto_address, query.royalty_rate*1000,
                                               "0x074C6794461525243043377094DbA36eed0A951B", tokenuri, user_db)
                        token_id = activate_buying[0]

                        query.current_fan_count += 1
                        query.save()
                        ticket_query_to_db = MintedTickets(event_id=query.id, owner_crypto_address=str(
                            buyer_crypto_address), owner_account=request.user, token_id=token_id, organizer=query.organizer)
                        ticket_query_to_db.save()
                        return JsonResponse({"status": "success"})
                except Exception as error2:
                    print(error2)
                    return JsonResponse({"status": "error"})
            else:
                return JsonResponse({"status": "failure"})
    return render(request, "Fan/GAMES.html")


@login_required(login_url='/login/')
def renderInventory(request):
    """
    Renders the inventory view for an authenticated user and retrieves their ticket collection.
    """

    minted_tickets_with_related_info = MintedTickets.objects.select_related(
        'event__organizer__club', 'event__opposite_team'
    ).filter(owner_account=request.user.pk)

    return render(request, 'Fan\MYTICKETS.html', {'collection': minted_tickets_with_related_info})


@login_required(login_url='/login/')
def renderKeys(request):
    """
    Renders the keys view for an authenticated user and retrieves their public and private keys.
    """
    user = request.user
    query_object = myFan.objects.get(pk=user)
    public_key = query_object.public_key
    private_key = query_object.private_key
    return render(request, "Fan\KEYS.html", {"pk": private_key, "publickey": public_key})


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


def Fan_to_address_Mapping(address):
    try:
        fan = myFan.objects.get(public_key=address)
        return fan.user
    except:
        return None


@csrf_exempt
def ReceiverContractEvents(request):
    print("yes")
    if request.method == 'POST':
        # Access the raw body of the request
        response_data = request.body.decode('utf-8')
        response_data = json.loads(response_data)
        print(response_data)
        # Parse the raw body JSON data into a Python dictionary
        if response_data['confirmed'] == True:
            from_address = response_data['txs'][0]['fromAddress']
            to_address = response_data['nftTransfers'][0]['to']
            token_id = response_data['nftTransfers'][0]['tokenId']
            block_number = response_data['block']['number']

            if from_address != "0x0000000000000000000000000000000000000000":
                user_hash = mainQrcode(
                    to_address, token_id)
                event_object = QrCodeChecking(name="QrCode", description="This is a Qr code",
                                              hash=user_hash, BlockNumber=block_number, token_id=token_id)
                event_object.save()
                token_id_query_info = MintedTickets.objects.get(
                    token_id=token_id)
                token_id_query_info.owner_crypto_address = to_address
                mappingfan = Fan_to_address_Mapping(to_address)
                token_id_query_info.owner_account = mappingfan
                token_id_query_info.save()

        # Print the extracted data

            print("From Address:", from_address)
            print("To Address:", to_address)
            print("Token ID:", token_id)
            print("Block Number:", block_number)
        return JsonResponse({"success": False}, status=200)
