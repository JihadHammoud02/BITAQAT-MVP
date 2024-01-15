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
from Club.models import Events, MintedTickets
from Fan.models import QrCodeChecking, myFan,Feedback
from authentication.models import myUsers
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage


@login_required(login_url='/login/')
def renderHomepage(request):
    """
    Renders the homepage view for an authenticated user.
    """
    user_db = myFan.objects.select_related('user').get(pk=request.user.pk)
    print(user_db.AuthWallet_public_key);
    return render(request, 'Fan/HOME.html')


@login_required(login_url='/login/')
def renderMarketplace(request):
    """
    Renders the marketplace view for an authenticated user and retrieves all available events.
    """
    current_datetime = timezone.now()
    all_events = Events.objects.select_related('organizer__club').select_related(
        'opposite_team').filter(datetime__gt=current_datetime)
    return render(request, 'Fan/GAMES.html', {'all_events': all_events})


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
        query = Events.objects.select_related(
            'organizer__club').select_related('opposite_team').get(pk=event_id)
        if query.current_fan_count < query.maximum_capacity:
            if count_tickets_in_accounts(request.user.pk, event_id) < query.maximum_ticket_per_account:
                buyer_crypto_address = user_db.public_key
                # try:
                tokenuri = upload_to_ipfs(str(query.organizer.club.name)+" vs "+str(query.opposite_team.name)+" #"+str(query.current_fan_count), "This is a match between " +
                                            str(query.organizer.club.name) + " and "+str(query.opposite_team.name)+" it will be played at "+str(query.place)+" on "+str(query.datetime.date())+" at "+str(query.datetime.time()), r"C:\Users\user\Desktop\BITAQAT\Tech\MVP\SOURCECODE\Bitaqat-MVP\Bitaqat\media\gre.jpg")
                # response = requests.get(tokenuri)
                # if response.status_code == 200:
                print(user_db.AuthWallet_public_key)
                activate_buying = main(buyer_crypto_address, query.royalty_rate,
                                        query.organizer.RoyaltyReceiverAddresse, tokenuri,user_db.AuthWallet_public_key,user_db.AuthWallet_private_key)
                
                token_id = activate_buying[0]

                query.current_fan_count += 1
                query.save()
                ticket_query_to_db = MintedTickets(event_id=query.id, owner_crypto_address=str(
                    buyer_crypto_address), owner_account=request.user, token_id=token_id, organizer=query.organizer)
                ticket_query_to_db.save()
                return JsonResponse({"status": "success"})
                # except Exception as error2:
                #     return JsonResponse({"status": "error"})
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

    return render(request, 'Fan/MYTICKETS.html', {'collection': minted_tickets_with_related_info})


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


def giveFeedback(request):
    if request.method == "POST":
        name=request.user.name
        email=request.user.email
        rating=request.POST.get('user-friendliness')
        q2=request.POST.get('user-friendliness4')
        q3=request.POST.get('user-friendliness2')
        q4=request.POST.getlist('user-friendliness3')
        number=''
        for i in q4:
            number=number+i

        q5=request.POST.get('user-friendliness6')
        text=request.POST.get('text')
        feedback=Feedback.objects.create(name=name,email=email,q1=rating,q2=q2,q3=q3,q4=int(number),q5=q5,q6=text)
        feedback.save()
    return render(request,"Feedback.html")

