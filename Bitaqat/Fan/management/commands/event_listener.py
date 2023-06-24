from web3 import Web3
from web3.middleware import geth_poa
from eth_account import Account
import requests
import time
import json
from django.core.management.base import BaseCommand
from multiprocessing import Process
from Fan.models import QrCodeChecking, myFan
from Fan.SmartContract import mainQrcode
from Club.models import MintedTickets
import django
from django.apps import apps


def detect_event():

    w3 = Web3(Web3.HTTPProvider(
        'https://polygon-mumbai.infura.io/v3/b0f53a900b384eb1924a4cc9785afa39'))
    w3.middleware_onion.inject(geth_poa.geth_poa_middleware, layer=0)

    abi = [{"inputs": [{"internalType": "string", "name": "_name", "type": "string"}, {"internalType": "string", "name": "_symbol", "type": "string"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "approved", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "operator", "type": "address"}, {"indexed": False, "internalType": "bool", "name": "approved", "type": "bool"}], "name": "ApprovalForAll", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "_fromTokenId", "type": "uint256"}, {"indexed": False, "internalType": "uint256", "name": "_toTokenId", "type": "uint256"}], "name": "BatchMetadataUpdate", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "_tokenId", "type": "uint256"}], "name": "MetadataUpdate", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"}, {"indexed": True, "internalType": "address", "name": "to", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Transfer", "type": "event"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "approve", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "getApproved", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "operator", "type": "address"}], "name": "isApprovedForAll", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint96", "name": "royalty_rate", "type": "uint96"}, {"internalType": "address",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           "name": "RoyaltyReceiver", "type": "address"}, {"internalType": "string", "name": "tokenuri", "type": "string"}], "name": "mint", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [], "name":"name", "outputs":[{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "ownerOf", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "uint256", "name": "salePrice", "type": "uint256"}], "name": "royaltyInfo", "outputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "safeTransferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "safeTransferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "operator", "type": "address"}, {"internalType": "bool", "name": "approved", "type": "bool"}], "name": "setApprovalForAll", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"symbol", "outputs":[{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "tokenURI", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "transferFrom", "outputs": [], "stateMutability":"nonpayable", "type":"function"}]

    # Contract information
    contract_address = "0x44872B49d25c1A3A22C432b3e42290dE9103e53b"
    # Replace with the ABI of your contract

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)

    # Set the starting block number
    last_object = QrCodeChecking.objects.last()
    starting_block = 36795836  # Set the appropriate starting block

    while True:

        latest_block = w3.eth.block_number

        # Get the transfer events since the last checked block
        events = contract_instance.events.Transfer().get_logs(
            fromBlock=starting_block+1, toBlock=latest_block)

        # Process the events
        for event in events:
            if event['args']['from'] != "0x0000000000000000000000000000000000000000":
                user_hash = mainQrcode(
                    event['args']['to'], event['args']['tokenId'])
                event_object = QrCodeChecking(name="QrCode", description="This is a Qr code",
                                              user_Hash=user_hash, BlockNumber=event['blockNumber'], Tokenid=event['args']['tokenId'])
                event_object.save()
                token_id_query_info = MintedTickets.objects.get(
                    token_id=event['args'['tokenId']])
                token_id_query_info.owner_crypto_address = event['args']['to']
                token_id_query_info.organizer = 0
                print(event)
                time.sleep(10)

        # Update the starting block for the next poll
        starting_block = latest_block
        print("listening")


class Command(BaseCommand):
    help = 'Starts the transfer event detector'

    def handle(self, *args, **options):
        detect_event()
