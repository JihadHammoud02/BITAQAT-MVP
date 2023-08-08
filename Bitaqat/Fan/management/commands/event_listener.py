import environ
import requests
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa
from django.core.management.base import BaseCommand
from Fan.models import QrCodeChecking, myFan
from Fan.SmartContract import mainQrcode
from Club.models import MintedTickets


def Fan_to_address_Mapping(address):
    try:
        fan = myFan.objects.get(public_key=address)
        return fan.user
    except:
        return None


env = environ.Env()
environ.Env.read_env()


def detect_event():

    w3 = Web3(HTTPProvider(env("WEB3PROVIDER")))
    w3.middleware_onion.inject(geth_poa.geth_poa_middleware, layer=0)

    # Contract information
    contract_address = env("CONTRACTADDRESS")
    # Replace with the ABI of your contract

    abi = [{"inputs": [], "stateMutability":"nonpayable", "type":"constructor"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "approved", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "operator", "type": "address"}, {"indexed": False, "internalType": "bool", "name": "approved", "type": "bool"}], "name": "ApprovalForAll", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "_fromTokenId", "type": "uint256"}, {"indexed": False, "internalType": "uint256", "name": "_toTokenId", "type": "uint256"}], "name": "BatchMetadataUpdate", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "_tokenId", "type": "uint256"}], "name": "MetadataUpdate", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "address", "name": "account", "type": "address"}], "name": "Paused", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"}, {"indexed": True, "internalType": "address", "name": "to", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Transfer", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "address", "name": "account", "type": "address"}], "name": "Unpaused", "type": "event"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "approve", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "getApproved", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "operator", "type": "address"}], "name": "isApprovedForAll", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"name", "outputs":[{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"owner", "outputs":[{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          "name": "tokenId", "type": "uint256"}], "name": "ownerOf", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"pause", "outputs":[], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [], "name":"paused", "outputs":[{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"renounceOwnership", "outputs":[], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "uint256", "name": "salePrice", "type": "uint256"}], "name": "royaltyInfo", "outputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint96", "name": "RoyaltyRate", "type": "uint96"}, {"internalType": "address", "name": "RoyaltyReceiver", "type": "address"}, {"internalType": "string", "name": "uri", "type": "string"}], "name": "safeMint", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "safeTransferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "safeTransferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "operator", "type": "address"}, {"internalType": "bool", "name": "approved", "type": "bool"}], "name": "setApprovalForAll", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"symbol", "outputs":[{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "tokenURI", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "transferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [], "name":"unpause", "outputs":[], "stateMutability":"nonpayable", "type":"function"}]

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)

    # Retrieve the Alchemy API key from environment variables
    alchemy_api_key = "2SdkCfNbRSjLN1lFT8MwWE1vJ-9r8NmX"

    # Set the starting block number
    last_object = QrCodeChecking.objects.last()
    starting_block = last_object.BlockNumber if last_object else 0

    while True:
        # Retrieve the latest block number
        latest_block = w3.eth.block_number

        # Get the transfer events since the last checked block using Alchemy's webhooks
        response = requests.get(
            f'https://webhooks.alchemyapi.io/v2/{alchemy_api_key}?onlyConfirmed=true&addresses={contract_address}&fromBlock={starting_block + 1}&toBlock={latest_block}&topics=0x8d40a64e7e712e79a3221e24a8df6549c6d26a7510c1e388d09c2c54a42c8b6c')

        if response.status_code == 200:
            events_data = response.json().get('data', [])
            for event_data in events_data:
                print(event_data)
        else:
            print(
                f"Error fetching events from Alchemy: {response.status_code} - {response.text}")

        # Update the starting block for the next poll
        starting_block = latest_block
        print("listening")


class Command(BaseCommand):
    help = 'Starts the transfer event detector'

    def handle(self, *args, **options):
        detect_event()
