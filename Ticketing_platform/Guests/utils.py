import requests
import json
import os
from Organizers.models import EventsticketsMinted
from asgiref.sync import sync_to_async
from moralis import evm_api
"""
FUNCTIONS RESPONSIBLE FOR EXTERNAL DATA GATHERING
"""



def jsonifyString(object):
    return json.loads(object)


@sync_to_async
def  mintNft(nftName,nftDescription,nftImg,toAddress):

    url = "https://api.nftport.xyz/v0/mints/easy/files?chain=polygon&name="+nftName+"&description="+nftDescription+"&mint_to_address="+toAddress
    working_directory = os.getcwd()
    files = {"file": (working_directory+"/media/"+nftImg  , open(working_directory+"/media/"+nftImg , "rb"), "image/jpg")}
    headers = {
        "accept": "application/json",
        "Authorization": "58ad0ea8-5abc-423d-bbcc-8ca3c344f2b8"
    }

    response_from_api : str =  requests.post(url, files=files, headers=headers)
    return jsonifyString(response_from_api.text)



def getTokenID(trxHASH):
    url = "https://api.nftport.xyz/v0/mints/"+trxHASH+"?chain=polygon"

    headers = {
        "accept": "application/json",
        "Authorization": "58ad0ea8-5abc-423d-bbcc-8ca3c344f2b8"
    }

    response =  requests.get(url, headers=headers)
    fetched_query=jsonifyString(response.text)
    print(fetched_query)
    return fetched_query['token_id']



def formatList(object):
    finalListe=[]
    for ele in object:
        finalListe.append(ele[0])
    return finalListe

def fetchNftsMetadata(userAddress):

    listTokens=formatList(EventsticketsMinted.objects.values_list("NFT_token_id"))
    collection=[]
    api_key = "bXnuNSkj87bbXsOr9k0b4TSsPXaerKj42dAfUi8dGyrvbVjRz4MZSjCPmGnUUlbM"
    params = {
        "address": userAddress, 
        "chain": "polygon", 
        "format": "decimal", 
        "limit": 20, 
        "token_addresses": [], 
        "cursor": "", 
        "normalizeMetadata": True, 
    }

    result = evm_api.nft.get_wallet_nfts(
        api_key=api_key,
        params=params,
    )
    for nft in result['result']:
        if nft['token_id'] in listTokens:
            nft_metadata=jsonifyString(nft['metadata'])
            collection.append({"image":nft_metadata['image'],'name':nft_metadata['name']})
    return collection
