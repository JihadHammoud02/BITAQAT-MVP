from brownie import accounts, MyNFT

def main():
    # Set the maximum price and royalty rate for the NFTs
    maxPrice = 1000
    royaltyRate = 5

    # Deploy the MyNFT contract
    nft_contract = MyNFT.deploy("MyNFT", "NFT", maxPrice, royaltyRate, {'from': accounts[0]})

    # Print the contract address
    print(f"MyNFT contract deployed at {nft_contract.address}")
