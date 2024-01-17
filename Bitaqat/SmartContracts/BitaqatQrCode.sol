// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";


contract BitaqatQrCode is  ERC721, ERC721URIStorage  {

        uint256 tokenId;

        constructor() ERC721("BitaqatQrCode", "BQC"){}


        function mintTicket(address to,string memory uri) public {
            _safeMint(to,tokenId);
            _setTokenURI(tokenId,uri);
            tokenId++;

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
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }


        


}