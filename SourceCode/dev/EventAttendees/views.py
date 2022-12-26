from django.shortcuts import render
from EventOrganizer.models import EventsCreated
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from SignUpAuth.models import Organizers
from EventOrganizer.models import ticketsMinted
from SignUpAuth.models import Attandees
from django.contrib.auth.models import User
import json
import time
import os
# Create your views here.


@login_required(login_url='/login/  ')
# """
# It renders the homepage.html template and passes the username of the logged in user to the template
# :param request: The request object is the first parameter to every view function. It contains
# information about the request that was made to the server, such as the HTTP method, the path, the
# headers, and the body
# :return: The request, the template, and the user's username.
# """
def Get_homepage(request):
    return render(request, 'EventAttendees\homepage.html', {"user_name": request.user.username})



@login_required(login_url='/login/  ')
def Get_profile_page(request):
    return render(request,'EventAttendees\profile.html')



@login_required(login_url='/login/  ')
def Get_Marketplace_Page(request):
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
    return render(request,'EventAttendees\Marketplace.html',{'all_events':all_events})


@login_required(login_url='/login/  ')
def Get_specific_event_page(request,event_id):
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
    print(event)
    return render(request,'EventAttendees\event_info_page.html',{'all_events':event})




def query_NFT_owner_from_blockchain(TOKEN_ID,CONTRACT_ADDRESS):


    url = "https://api.simplehash.com/api/v0/nfts/polygon/"+str(CONTRACT_ADDRESS)+"/"+str(TOKEN_ID)

    headers = {
        "accept": "application/json",
        "X-API-KEY": "sh_sk1_Z4jhWXXBE09em"
    }

    response = requests.get(url, headers=headers)
    response=json.loads(response.text)
    print(response)
    owner_address=response['owners'][-1]['owner_address']

    return owner_address


def match_address_with_account(NFT_ADDRESS):
    attendee=Attandees.objects.get(public_crypto_address=NFT_ADDRESS)
    user=User.objects.get(attendee.pk)
    return user.username


def get_token_id(TRX_HASH):

    url = "https://api.nftport.xyz/v0/mints/0x2fe7ad6c6afc25498bbbb0b6a4d190e0a7735bc5acf02337a40372c2d9c1f85e?chain=polygon"

    headers = {
        "accept": "application/json",
        "Authorization": "1e772e66-b2a4-46e7-afa2-28e5ef7ca99f"
    }

    response = requests.get(url, headers=headers)

    fetched_query_string=response.text
    fetched_query=json.loads(fetched_query_string)
    print(fetched_query)
    return fetched_query['token_id']

@login_required(login_url='/login/  ')
def mint_nft(request,event_id):
    user_db=Attandees.objects.get(pk=request.user.pk)
    event_query=EventsCreated.objects.get(pk=event_id)
    event={}
    event['name']=event_query.event_name
    event['desc']=event_query.event_description
    event['banner']=event_query.event_banner
    event['available_places']=event_query.event_maximum_capacity-event_query.number_of_current_guests
    event['organizer']=event_query.event_organizer.username 

    url = "https://api.nftport.xyz/v0/mints/easy/files?chain=polygon&name="+event['name']+str(event['available_places'])+"&description="+event['desc']+"&mint_to_address="+str(user_db.public_crypto_address)
    working_directory = os.getcwd()
    files = {"file": (working_directory+"/media/"+str(event['banner'])  , open(working_directory+"/media/"+str(event['banner']) , "rb"), "image/jpg")}
    headers = {
        "accept": "application/json",
        "Authorization": "1e772e66-b2a4-46e7-afa2-28e5ef7ca99f"
    }

    response = requests.post(url, files=files, headers=headers)

    print(response.text)

    # This is done for technical reasons 
    url2 = "https://api.nftport.xyz/v0/mints/easy/files?chain=polygon&name="+"Forwarder"+"&description="+event['desc']+"&mint_to_address=0x3B9019DC197393d4425e51d9fCd94600d523Bc89"
    headers2 = {
        "accept": "application/json",
        "Authorization": "1e772e66-b2a4-46e7-afa2-28e5ef7ca99f"
    }

    event_query.number_of_current_guests+=1

    response2 = requests.post(url2, headers=headers2)

    fetched_query_string=response.text
    fetched_query=json.loads(fetched_query_string)
    CONTRACT_ADDRESS=str(fetched_query['contract_address'])
    TRX_HASH=str(fetched_query['transaction_hash'])
    time.sleep(5)
    TOKEN_ID=get_token_id(TRX_HASH)
    NFT_owner_address=query_NFT_owner_from_blockchain(TOKEN_ID,CONTRACT_ADDRESS)
    ticket_query_to_db=ticketsMinted(event_query,event_query.event_name,NFT_owner_address,NFT_owner_account=match_address_with_account(NFT_owner_address))
    ticket_query_to_db.save()



    return Get_Marketplace_Page(request)

