from django.shortcuts import render
import datetime
from Club.models import EventsCreated
from Club.models import EventsticketsMinted
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import myUsers
from Fan.models import myFan,loyalFan
import time
from .utils import fetchNftsMetadata,getTokenID
import asyncio
from django.http import HttpResponseRedirect
from Club.query import queryEvents,queryAttEvents
from django.urls import reverse
from .SmartContract import main,upload_to_ipfs,TokenId


@login_required(login_url='/login/  ')
def renderHomepage(request):
    print(request.user)
    eventNumber=queryEvents()[1]
    attandeesNumber=len(myFan.objects.all().filter())
    ticketsNumber=len(EventsticketsMinted.objects.all().filter())
    return render(request, 'Fan\homepage.html', {"user_name": request.user.username,"eventNumber":eventNumber,"attandeesNumber":attandeesNumber,'ticketsNumber':ticketsNumber})




@login_required(login_url='/login/  ')
def renderMarketplace(request):
    all_events=queryEvents()[0]
    user_db=myFan.objects.get(pk=request.user.pk)
    return render(request,'Fan\Marketplace.html',{'all_events':all_events})



@login_required(login_url='/login/  ')
def renderSpecificEventPage(request,event_id):
    # GETTING EVENTS DATA FROM DATABASE
    event=queryEvents("pk",event_id)
    return render(request,'Fan\event_info_page.html',{'all_events':event[0][0]})



#Search in the database who owns this address
def match_address_with_account(ownedPublicAddress):
    queriedGuest=myFan.objects.get(public_crypto_address=ownedPublicAddress)
    user=myUsers.objects.get(pk=queriedGuest.user_id)
    return user


def buyTicket(request,event_id):
    user_db=myFan.objects.get(pk=request.user.pk)
    query=EventsCreated.objects.get(pk=event_id)
    buyer_crypto_address=user_db.public_crypto_address
    print(buyer_crypto_address)
    #calling the minting function 
    tx_hash=main(buyer_crypto_address,query.royaltyRate*1000,"0x074C6794461525243043377094DbA36eed0A951B",upload_to_ipfs(str(query.Team1Name)+" vs "+str(query.Team2Name)+" #"+str(query.number_of_current_Fan),"This is a match between "+
    str(query.Team1Name) +" and "+str(query.Team2Name)+" it will be played at "+str(query.event_place)+" on "+str(query.event_date_time.date())+" at "+str(query.event_date_time.time()),query.Team1Logo.path))
    query.number_of_current_Fan+=1
    query.save()
    ticket_query_to_db=EventsticketsMinted(event_id=query,NFT_owner_address=str(buyer_crypto_address),NFT_owner_account=match_address_with_account(buyer_crypto_address),NFT_token_id=None,organizer=query.event_organizer)
    ticket_query_to_db.save()

    loyaltyQuery=loyalFan.objects.filter(**{'organizer':query.event_organizer,"guest":request.user.pk})
    if len(loyaltyQuery)!=0:
        loyaltyQuery[0].eventsCount+=1
        loyaltyQuery[0].save()
    else:
        loyalty=loyalFan(guest=request.user,organizer=query.event_organizer,eventsCount=1)
        loyalty.save()



    return HttpResponseRedirect(reverse('Fan:renderMarketplace'))




def getTokenId(request,tx_hash):
    try:
        tokenid=TokenId(tx_hash=tx_hash)
        

    except:
        return {"message":"404"}




def renderInventory(request):
    attendee=myFan.objects.get(user_id=request.user.pk)
    userAddress=attendee.public_crypto_address
    collection=fetchNftsMetadata(userAddress)
    return render(request,'Fan\Inventory.html',{"collection":collection})



