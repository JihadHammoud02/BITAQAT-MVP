from django.shortcuts import render
import datetime
from Organizers.models import EventsCreated
from Organizers.models import ticketsMinted
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import myUsers
from Guests.models import myGuests
import time
from .utils import mintNft, getTokenID, jsonifyString, fetchNftsMetadata
import asyncio

from Organizers.query import queryEvents




@login_required(login_url='/login/  ')
def renderHomepage(request):
    eventNumber=queryEvents()[1]
    attandeesNumber=len(myGuests.objects.all().filter())
    ticketsNumber=len(ticketsMinted.objects.all().filter())
    return render(request, 'Guests\homepage.html', {"user_name": request.user.username,"eventNumber":eventNumber,"attandeesNumber":attandeesNumber,'ticketsNumber':ticketsNumber})


@login_required(login_url='/login/  ')
def renderProfile(request):
    return render(request,'Guests\profile.html')



@login_required(login_url='/login/  ')
def renderMarketplace(request):
    all_events=queryEvents()[0]
    return render(request,'Guests\Marketplace.html',{'all_events':all_events})



@login_required(login_url='/login/  ')
def renderSpecificEventPage(request,event_id):
    # GETTING EVENTS DATA FROM DATABASE
    event=queryEvents("pk",event_id)
    return render(request,'Guests\event_info_page.html',{'all_events':event[0][0]})



#Search in the database who owns this address
def match_address_with_account(ownedPublicAddress):
    queriedGuest=myGuests.objects.get(public_crypto_address=ownedPublicAddress)
    user=myUsers.objects.get(pk=queriedGuest.user_id)
    return user


async def buyTicket(request,event_id):
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
    TOKEN_ID=getTokenID(TRX_HASH) #We need to save the Token id in our database to be able to later on query the address of the owner of this Token from the Blockchain





    ticket_query_to_db=ticketsMinted(event_id=query,NFT_owner_address=str(buyer_crypto_address),NFT_owner_account=match_address_with_account(buyer_crypto_address),NFT_token_id=TOKEN_ID)
    ticket_query_to_db.save()
    return renderMarketplace(request)


def renderInventory(request):
    attendee=myGuests.objects.get(user_id=request.user.pk)
    userAddress=attendee.public_crypto_address
    collection=fetchNftsMetadata(userAddress)
    return render(request,'Guests\Inventory.html',{"collection":collection})


