from web3 import Web3
from web3.middleware import geth_poa
from eth_account import Account
import requests
import time
import json
import hashlib
import random
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files import File
import tempfile
# Connect to the blockchain network (e.g., Ganache local network)
w3 = Web3(Web3.HTTPProvider(
    'https://polygon-mumbai.infura.io/v3/b0f53a900b384eb1924a4cc9785afa39'))
w3.middleware_onion.inject(geth_poa.geth_poa_middleware, layer=0)

abi = [{"inputs": [{"internalType": "string", "name": "_name", "type": "string"}, {"internalType": "string", "name": "_symbol", "type": "string"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "approved", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "operator", "type": "address"}, {"indexed": False, "internalType": "bool", "name": "approved", "type": "bool"}], "name": "ApprovalForAll", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "_fromTokenId", "type": "uint256"}, {"indexed": False, "internalType": "uint256", "name": "_toTokenId", "type": "uint256"}], "name": "BatchMetadataUpdate", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "_tokenId", "type": "uint256"}], "name": "MetadataUpdate", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"}, {"indexed": True, "internalType": "address", "name": "to", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Transfer", "type": "event"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "approve", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "getApproved", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "operator", "type": "address"}], "name": "isApprovedForAll", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint96", "name": "royalty_rate", "type": "uint96"}, {"internalType": "address",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       "name": "RoyaltyReceiver", "type": "address"}, {"internalType": "string", "name": "tokenuri", "type": "string"}], "name": "mint", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [], "name":"name", "outputs":[{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "ownerOf", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "uint256", "name": "salePrice", "type": "uint256"}], "name": "royaltyInfo", "outputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "safeTransferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "safeTransferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "operator", "type": "address"}, {"internalType": "bool", "name": "approved", "type": "bool"}], "name": "setApprovalForAll", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"symbol", "outputs":[{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "tokenURI", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "transferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}]

# Contract information
contract_address = "0x44872B49d25c1A3A22C432b3e42290dE9103e53b"
# Replace with the ABI of your contract

abi2 = [{"inputs": [{"internalType": "string", "name": "_name", "type": "string"}, {"internalType": "string", "name": "_symbol", "type": "string"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "approved", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "operator", "type": "address"}, {"indexed": False, "internalType": "bool", "name": "approved", "type": "bool"}], "name": "ApprovalForAll", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "_fromTokenId", "type": "uint256"}, {"indexed": False, "internalType": "uint256", "name": "_toTokenId", "type": "uint256"}], "name": "BatchMetadataUpdate", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "_tokenId", "type": "uint256"}], "name": "MetadataUpdate", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"}, {"indexed": True, "internalType": "address", "name": "to", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Transfer", "type": "event"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "approve", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "getApproved", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "operator", "type": "address"}], "name": "isApprovedForAll", "outputs": [{"internalType": "bool",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "string", "name": "tokenuri", "type": "string"}], "name": "mint", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [], "name":"name", "outputs":[{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "ownerOf", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "safeTransferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "safeTransferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "operator", "type": "address"}, {"internalType": "bool", "name": "approved", "type": "bool"}], "name": "setApprovalForAll", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"symbol", "outputs":[{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "tokenURI", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "transferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}]
contract_QrCode_address = "0x968671f7A945a3b2ef833135ea5e6eE117Fd135D"

proj_id = "2Qrs6mmPXUPVgyBsaK4GEO6JDai"
proj_secret = "6c4a430ca570bfc603e0c2b9cd1699a7"

private_key = 'ce136daa0b7ffc83cf1ac6aae719e25e31037b117913b751a0726a551a5e9d17'
from_address = '0x9cd4D8EcA8954e55ea1B8d194B2A4E5dfb4EE7dc'
# Function to send a signed transaction


def send_signed_transaction(signed_transaction):
    response = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return response.hex()
# Example usage


def main(recipient_address, quantity, royaltyrec, tokenuri):

    # Request test tokens from the Polygon Mumbai Testnet Faucet
    faucet_url = 'https://faucet.matic.network/transfer'
    response = requests.post(faucet_url, data={'address': from_address})
    if response.status_code == 200:
        print('Test tokens received from the faucet.')

        # Load contract instance
        contract_instance = w3.eth.contract(address=contract_address, abi=abi)

        # Construct the transaction data
        transaction_data = contract_instance.functions.mint(recipient_address, quantity, royaltyrec, tokenuri).build_transaction({
            'from': from_address,
            'value': 0,
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(from_address),
            'chainId': 80001  # Chain ID of the Polygon Mumbai chain
        })
        print(transaction_data)

        # Sign the transaction locally
        signed_transaction = Account.sign_transaction(
            transaction_data, private_key)

        # Send the signed transaction
        transaction_hash = send_signed_transaction(signed_transaction)

        print('Transaction sent. Hash:', transaction_hash)
    else:
        print('Failed to request test tokens from the faucet.')
    tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    token_id = w3.to_int(tx_receipt['logs'][0]['topics'][3])
    return token_id


def upload_to_ipfs(name, description, image_path):
    # Read the image file
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Upload the image to IPFS
    response = requests.post('https://ipfs.infura.io:5001/api/v0/add',
                             auth=(proj_id, proj_secret), files={'file': image_data})
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
    response = requests.post('https://ipfs.infura.io:5001/api/v0/add',
                             auth=(proj_id, proj_secret), files=metadata_file)
    print(response.text)
    metadata_hash = response.json()['Hash']

    # Return the URI for the metadata JSON file
    return f'https://ipfs.io/ipfs/{metadata_hash}'


def MintQrCode(tokenuri, recipient_address):
 # Request test tokens from the Polygon Mumbai Testnet Faucet
    faucet_url = 'https://faucet.matic.network/transfer'
    response = requests.post(faucet_url, data={'address': from_address})
    if response.status_code == 200:
        print('Test tokens received from the faucet.')

        # Load contract instance
        contract_instance = w3.eth.contract(
            address=contract_QrCode_address, abi=abi2)

        # Construct the transaction data
        transaction_data = contract_instance.functions.mint(recipient_address, tokenuri).build_transaction({
            'from': from_address,
            'value': 0,
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(from_address),
            'chainId': 80001  # Chain ID of the Polygon Mumbai chain
        })
        print(transaction_data)

        # Sign the transaction locally
        signed_transaction = Account.sign_transaction(
            transaction_data, private_key)

        # Send the signed transaction
        transaction_hash = send_signed_transaction(signed_transaction)

        print('Transaction sent. Hash:', transaction_hash)
    else:
        print('Failed to request test tokens from the faucet.')


def hashData(receiver_address, token_id):
    input_data = receiver_address + str(token_id) + str(time.time())
    # Convert the input string to a list of characters
    input_data = list(input_data)
    random.shuffle(input_data)  # Shuffle the characters randomly
    # Convert the shuffled characters back to a string
    shuffled_data = ''.join(input_data)

    hashed_data = hashlib.sha256(shuffled_data.encode()).hexdigest()
    return hashed_data


def generate_qr_code(hashed_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(hashed_data)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        qr_image.save(temp_file.name)
    print(temp_file.name)
    ipfs_link = upload_to_ipfs("Qrcode1", "This is a Qrcode", temp_file.name)
    print(ipfs_link)
    # Return the saved model instance if needed
    return ipfs_link


def mainQrcode(receiver_address, token_id):
    hashed_data = hashData(
        receiver_address=receiver_address, token_id=token_id)
    Qrcodelink = generate_qr_code(hashed_data)
    time.sleep(5)
    mintedQrcode = MintQrCode(
        tokenuri=Qrcodelink, recipient_address=receiver_address)
    return hashed_data


def get_balance(wallet_address):
    balance_wei = w3.eth.get_balance(wallet_address)

# Convert the balance from Wei to Ether
    balance_ether = w3.from_wei(balance_wei, 'ether')

    # Fetch the current Ether price in USD from an external API (e.g., CoinGecko)
    response = requests.get(
        'https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd')
    data = response.json()
    matic_price_usd = data['matic-network']['usd']
    # Calculate the balance in USD
    balance_usd = float(balance_ether) * matic_price_usd

    return round(balance_usd, 2)