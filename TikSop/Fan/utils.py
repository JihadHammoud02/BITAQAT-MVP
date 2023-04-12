import requests
import json
import os
from Club.models import EventsticketsMinted
from asgiref.sync import sync_to_async
from moralis import evm_api
"""
FUNCTIONS RESPONSIBLE FOR EXTERNAL DATA GATHERING
"""



def jsonifyString(object):
    return json.loads(object)




@sync_to_async
def  mintNft(nftName,nftDescription,nftImg,toAddress):

    url = "https://staging.crossmint.io/api/2022-06-09/collections/default-polygon/nfts"

    payload = {
        "recipient": "polygon:"+toAddress,
        "metadata": {
            "name": nftName,
            "image": nftImg,
            "description": nftDescription
        }
    }
    headers = {
        "content-type": "application/json",
        "x-client-secret": "sk_test.iSjwcEK4.7miWBYLfMymwL5Hm9JMo30QzVUN75NTN",
        "x-project-id": "7b44996c-8c2b-4875-a677-8b3e2627ed7a"
    }

    response = requests.post(url, json=payload, headers=headers)

    fetchedResponse=jsonifyString(response.text)
    print("minted Successfully")
    return fetchedResponse['id']



def getTokenID(CrossMintId):  

    pending=True  
    while pending==True:
        url = "https://staging.crossmint.io/api/2022-06-09/collections/default-polygon/nfts/"+CrossMintId

        headers = {
            "x-client-secret": "sk_test.iSjwcEK4.7miWBYLfMymwL5Hm9JMo30QzVUN75NTN",
            "x-project-id": "7b44996c-8c2b-4875-a677-8b3e2627ed7a"
         }

        response = requests.get(url, headers=headers)
        fetchedResponse=jsonifyString(response.text)
        if fetchedResponse['onChain']["status"]!="pending":
            pending=False
    print(fetchedResponse)
    return fetchedResponse["onChain"]["tokenId"]



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
        "chain": "mumbai", 
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
            print(nft_metadata)
            collection.append({"image":nft_metadata['image'],'name':nft_metadata['name']})
    return collection



def getOwners(ContractAddress=0,TokenID=0):
    api_key = "bXnuNSkj87bbXsOr9k0b4TSsPXaerKj42dAfUi8dGyrvbVjRz4MZSjCPmGnUUlbM"
    params = {
        "address": "0x37A310401d58C9545da86ff66Aa953BAE6FB6272",
        "token_id": "26976",
        "chain": "polygon",
        "format": "decimal",
        # "limit": 100,
        # "cursor": "",
    }

    result = evm_api.nft.get_nft_transfers(
        api_key=api_key,
        params=params,
    )

    return result