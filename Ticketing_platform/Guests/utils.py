import requests
import json
import os

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
        "Authorization": "1e772e66-b2a4-46e7-afa2-28e5ef7ca99f"
    }

    response_from_api : str =  requests.post(url, files=files, headers=headers)
    return jsonifyString(response_from_api.text)



def getTokenID(trxHASH):
    url = "https://api.nftport.xyz/v0/mints/"+trxHASH+"?chain=polygon"

    headers = {
        "accept": "application/json",
        "Authorization": "8fe0e991-316b-4c53-937b-2dec08b030af"
    }

    response =  requests.get(url, headers=headers)
    fetched_query=jsonifyString(response.text)
    return fetched_query['token_id']



def fetchNftsMetadata(userAddress):
        url = "https://api.nftport.xyz/v0/accounts/"+userAddress+"?chain=polygon&page_size=50&include=metadata"

        headers = {
            "accept": "application/json",
            "Authorization": "de43bb2f-aea3-46e2-986e-0fe2c7f58ceb"
        }

        response = requests.get(url, headers=headers)

        
        fetched_query=jsonifyString(response.text)

        #getting all NFTs metadata
        collection=[]
        liste_of_names=[]
        for nft in fetched_query['nfts']:
            if nft['name']!=None and  nft['name'] not in liste_of_names: # There is a glitch where some nfts are labeled as None, it may be resolved later on in production when we choose another API.
                collection.append({'image':nft['metadata']['image'], 'name':nft['metadata']['name']})
                liste_of_names.append(nft['metadata']['name'])
        return collection
