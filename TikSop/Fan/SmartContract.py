from web3 import Web3
from web3.middleware import geth_poa
from eth_account import Account
import requests
import time
import json

# Connect to the blockchain network (e.g., Ganache local network)
w3 = Web3(Web3.HTTPProvider('https://polygon-mumbai.infura.io/v3/b0f53a900b384eb1924a4cc9785afa39'))
w3.middleware_onion.inject(geth_poa.geth_poa_middleware   , layer=0)

abi=[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"MetadataUpdate","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint96","name":"RoyaltyRate","type":"uint96"},{"internalType":"address","name":"RoyaltyReceiver","type":"address"},{"internalType":"string","name":"tokenuri","type":"string"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"salePrice","type":"uint256"}],"name":"royaltyInfo","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}]

# Contract information
contract_address = "0x44872B49d25c1A3A22C432b3e42290dE9103e53b"
 # Replace with the ABI of your contract


proj_id="2Qrs6mmPXUPVgyBsaK4GEO6JDai"
proj_secret="6c4a430ca570bfc603e0c2b9cd1699a7"


# Function to send a signed transaction
def send_signed_transaction(signed_transaction):
    response = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return response.hex()
# Example usage
def main(recipient_address,quantity,royaltyrec,tokenuri):
    private_key = 'ce136daa0b7ffc83cf1ac6aae719e25e31037b117913b751a0726a551a5e9d17'
    from_address = '0x9cd4D8EcA8954e55ea1B8d194B2A4E5dfb4EE7dc'

    # Request test tokens from the Polygon Mumbai Testnet Faucet
    faucet_url = 'https://faucet.matic.network/transfer'
    response = requests.post(faucet_url, data={'address': from_address})
    if response.status_code == 200:
        print('Test tokens received from the faucet.')

        # Load contract instance
        contract_instance = w3.eth.contract(address=contract_address, abi=abi)

        # Construct the transaction data
        transaction_data = contract_instance.functions.mint(recipient_address, quantity,royaltyrec,tokenuri).build_transaction({
            'from': from_address,
            'value': 0,
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(from_address),
            'chainId': 80001  # Chain ID of the Polygon Mumbai chain
        })
        print(transaction_data)

        # Sign the transaction locally
        signed_transaction = Account.sign_transaction(transaction_data, private_key)

        # Send the signed transaction
        transaction_hash = send_signed_transaction(signed_transaction)

        print('Transaction sent. Hash:', transaction_hash)
    else:
        print('Failed to request test tokens from the faucet.')
    tx_receipt=w3.eth.wait_for_transaction_receipt(transaction_hash)
    token_id = w3.to_int(tx_receipt['logs'][0]['topics'][3])
    print(token_id)

    return token_id





def upload_to_ipfs(name, description, image_path):
    # Read the image file
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Upload the image to IPFS
    response = requests.post('https://ipfs.infura.io:5001/api/v0/add',auth=(proj_id, proj_secret), files={'file': image_data})
    image_hash = response.json()['Hash']

    # Create the metadata dictionary
    metadata = {
        'image': f'https://ipfs.io/ipfs/{image_hash}',
        'name': name,
        'description': description
    }

    # Convert metadata to JSON string
    metadata_json = json.dumps(metadata)
    metadata_file = {'file': metadata_json}

    # Upload the metadata to IPFS
    response = requests.post('https://ipfs.infura.io:5001/api/v0/add',auth=(proj_id, proj_secret), files=metadata_file)
    print(response.text)
    metadata_hash = response.json()['Hash']

    # Return the URI for the metadata JSON file
    return f'https://ipfs.io/ipfs/{metadata_hash}'


# FAN1="0x7F3cB754548a06c009c36692e310F14E8Dea4fe0"
# FAN2="0x14BD09d735466E4FC3FFf895eCF17b16035dFC80"
# FAN3="0x5Fb257A2488aB3e9aD51f300A3d6D901Ce481Fc8"
# FAN4="0x2E2F118bBC3c7452a1ef7E0BDC7E51aFeBfaC868"
# FAN5="0xfA014C0ebcEd73D48aea6422A1869521394E49dE"
# ALIttihadRoyaltyVault="0x074C6794461525243043377094DbA36eed0A951B"
# ALNASSRROYAlTYVAULT="0x3B9019DC197393d4425e51d9fCd94600d523Bc89"

