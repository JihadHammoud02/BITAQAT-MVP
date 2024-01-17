// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";


contract Bitaqat is  ERC721, ERC721URIStorage, ERC721Royalty  {

        uint256 tokenId;
        address owner=0x9cd4D8EcA8954e55ea1B8d194B2A4E5dfb4EE7dc;

        constructor() ERC721("Bitaqat", "BTQ"){}


        function mintTicket(address to,uint96 royaltyRate, address RoyaltyReceiver,string memory uri,bytes32 _messageHash, uint8 _v, bytes32 _r, bytes32 _s) public {
            require(verifySignature(_messageHash,_v,_r,_s) == owner);
            _safeMint(to,tokenId);
            _setTokenRoyalty(tokenId,RoyaltyReceiver,royaltyRate*100);
            _setTokenURI(tokenId,uri);
            tokenId++;

        }

        function verifySignature(bytes32 _messageHash, uint8 _v, bytes32 _r, bytes32 _s) public pure returns (address) {
            return ecrecover(_messageHash, _v, _r, _s);
        }

        function test() public view returns (address){
            return msg.sender;
        }


        function tokenURI(uint256 tokenid)
        public
        view
        override (ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenid);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage,ERC721Royalty)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }


        


}