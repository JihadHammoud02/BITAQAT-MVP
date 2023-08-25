from moralis import evm_api
"""
FUNCTIONS RESPONSIBLE FOR EXTERNAL DATA GATHERING
"""


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
    print(TokenID)
    api_key = "bXnuNSkj87bbXsOr9k0b4TSsPXaerKj42dAfUi8dGyrvbVjRz4MZSjCPmGnUUlbM"
    params = {
        "chain": "mumbai",
        "format": "decimal",
        "address": "0xE886d763A55575c533123c621C29D9E286D60631",
        "token_id": TokenID
    }

    try:

        result = evm_api.nft.get_nft_transfers(
            api_key=api_key,
            params=params,

        )

        if len(result['result']) > 0:
            if result['result'][0]['from_address'] != "0x0000000000000000000000000000000000000000":
                count = count+1

    except:
        pass

    return count
