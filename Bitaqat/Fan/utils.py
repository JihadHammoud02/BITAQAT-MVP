import requests
import json
import os
from Club.models import MintedTickets
from asgiref.sync import sync_to_async
from moralis import evm_api
"""
FUNCTIONS RESPONSIBLE FOR EXTERNAL DATA GATHERING
"""


def jsonifyString(object):
    return json.loads(object)


def getTokenID(CrossMintId):

    pending = True
    while pending == True:
        url = "https://staging.crossmint.io/api/2022-06-09/collections/default-polygon/nfts/"+CrossMintId

        headers = {
            "x-client-secret": "sk_test.iSjwcEK4.7miWBYLfMymwL5Hm9JMo30QzVUN75NTN",
            "x-project-id": "7b44996c-8c2b-4875-a677-8b3e2627ed7a"
        }

        response = requests.get(url, headers=headers)
        fetchedResponse = jsonifyString(response.text)
        print(fetchedResponse)
        if fetchedResponse['onChain']["status"] != "pending":
            pending = False
    print(fetchedResponse)
    return fetchedResponse["onChain"]["tokenId"]


def formatList(object):
    finalListe = []
    for ele in object:
        finalListe.append(ele[0])
    return finalListe


def fetchNftsMetadata(userAddress):

    listTokens = formatList(MintedTickets.objects.values_list("token_id"))
    collection = []
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
            nft_metadata = jsonifyString(nft['metadata'])
            collection.append(
                {"image": nft_metadata['image'], 'name': nft_metadata['name'], "tokenid": nft['token_id']})
    return collection


def getOwners(ContractAddress, TokenID):
    api_key = "bXnuNSkj87bbXsOr9k0b4TSsPXaerKj42dAfUi8dGyrvbVjRz4MZSjCPmGnUUlbM"
    params = {
        "address": ContractAddress,
        "token_id": TokenID,
        "chain": "mumbai",
        "format": "decimal",
        # "limit": 100,
        # "cursor": "",
    }

    result = evm_api.nft.get_nft_transfers(
        api_key=api_key,
        params=params,
    )

    return result


def VolumneTraded(TokenID):
    count = 0
    api_key = "bXnuNSkj87bbXsOr9k0b4TSsPXaerKj42dAfUi8dGyrvbVjRz4MZSjCPmGnUUlbM"
    params = {
        "chain": "mumbai",
        "format": "decimal",
        "address": "0x44872B49d25c1A3A22C432b3e42290dE9103e53b",
        "token_id": TokenID
    }

    result = evm_api.nft.get_nft_transfers(
        api_key=api_key,
        params=params,

    )
    if result['result'][0]['from_address'] != "0x0000000000000000000000000000000000000000":
        count = count+1

    return count
