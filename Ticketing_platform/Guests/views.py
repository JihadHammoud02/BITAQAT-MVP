from django.shortcuts import render
import requests
from Organizers.models import EventsCreated
from Organizers.models import ticketsMinted
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import myUsers
from Guests.models import myGuests
from django.http import HttpResponseBadRequest
import time
from .utils import mintNft, getTokenID, jsonifyString, fetchNftsMetadata
import asyncio
import aiohttp




@login_required(login_url='/login/  ')
def renderHomepage(request):
    return render(request, 'Guests\homepage.html', {"user_name": request.user.username})


@login_required(login_url='/login/  ')
def renderProfile(request):
    return render(request,'Guests\profile.html')


@login_required(login_url='/login/  ')
def renderMarketplace(request):
    list_of_all_events=EventsCreated.objects.all()
    all_events=[]
    event={}
    for eve in list_of_all_events:
        event['id']=eve.pk
        event['name']=eve.event_name
        event['date/time']=eve.event_date_time
        event['desc']=eve.event_description
        event['banner']=eve.event_banner
        event['price']=eve.event_ticket_price
        event['maxcap']=eve.event_maximum_capacity
        event['available_places']=eve.event_maximum_capacity-eve.number_of_current_guests
        event['organizer']=eve.event_organizer
        all_events.append(event)
        event={}
    print(request.user.is_Organizer)
    if request.user.is_Organizer:
         return render(request,'Organizers\Marketplace.html',{'all_events':all_events})
    return render(request,'Guests\Marketplace.html',{'all_events':all_events})



@login_required(login_url='/login/  ')
def renderSpecificEventPage(request,event_id):
    event_query=EventsCreated.objects.get(pk=event_id)
    event={}
    event['id']=event_query.pk
    event['name']=event_query.event_name
    event['datetime']=str(event_query.event_date_time)
    event['desc']=event_query.event_description
    event['banner']=event_query.event_banner
    event['price']=event_query.event_ticket_price
    event['available_places']=event_query.event_maximum_capacity-event_query.number_of_current_guests
    event['organizer']=event_query.event_organizer.username
    return render(request,'Guests\event_info_page.html',{'all_events':event})



#Search in the database who owns this address
def match_address_with_account(ownedPublicAddress):
    queriedGuest=myGuests.objects.get(public_crypto_address=ownedPublicAddress)
    user=myUsers.objects.get(pk=queriedGuest.user_id)
    return user


async def buyTicket(request,event_id):
    start_time=time.time()
    user_db=myGuests.objects.get(pk=request.user.pk)
    query=EventsCreated.objects.get(pk=event_id)
    
    
    number=str(query.event_maximum_capacity-query.number_of_current_guests)
    #calling the minting function 
    apiResponse=asyncio.ensure_future(mintNft(query.event_name+number,query.event_description,str(query.event_banner),user_db.public_crypto_address,))

    #updating the number of guests of the event in the db
    query.number_of_current_guests+=1
    query.save()
    await asyncio.wait([apiResponse])
    apiResponse=apiResponse.result()
        #getting the transaction hash to use it to get the Token id of the minted NFT
    TRX_HASH=str(apiResponse['transaction_hash'])
    buyer_crypto_address=user_db.public_crypto_address

    time.sleep(5)
    print(time.time()-start_time)
    TOKEN_ID=getTokenID(TRX_HASH) #We need to save the Token id in our database to be able to later on query the address of the owner of this Token from the Blockchain





    ticket_query_to_db=ticketsMinted(event_id=query,NFT_owner_address=str(buyer_crypto_address),NFT_owner_account=match_address_with_account(buyer_crypto_address),NFT_token_id=TOKEN_ID)
    ticket_query_to_db.save()
    return renderMarketplace(request)


def renderInventory(request):
    attendee=myGuests.objects.get(user_id=request.user.pk)
    userAddress=attendee.public_crypto_address
    collection=fetchNftsMetadata(userAddress)
    return render(request,'Guests\Inventory.html',{"collection":collection})


