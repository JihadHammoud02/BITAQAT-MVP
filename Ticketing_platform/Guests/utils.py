import requests
import json
import os
from Organizers.models import EventsticketsMinted
from asgiref.sync import sync_to_async

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
        url = "https://api.nftport.xyz/v0/accounts/"+userAddress+"?chain=polygon&page_size=50&include=metadata"

        headers = {
            "accept": "application/json",
            "Authorization": "58ad0ea8-5abc-423d-bbcc-8ca3c344f2b8"
        }

        response = requests.get(url, headers=headers)

        listTokens=formatList(EventsticketsMinted.objects.values_list('NFT_token_id'))
        fetched_query=jsonifyString(response.text)
        print(listTokens)

        #getting all NFTs metadata
        collection=[]
        liste_of_names=[]
        for nft in fetched_query['nfts']:
            print(nft['name'])
            if nft['name']!=None and  nft['name'] not in liste_of_names and nft['token_id'] in listTokens:  # There is a glitch where some nfts are labeled as None, it may be resolved later on in production when we choose another API.
                collection.append({'image':nft['metadata']['image'], 'name':nft['metadata']['name']})
                liste_of_names.append(nft['metadata']['name'])
        return collection
