// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol"; //a ajuster
import "@openzeppelin/contracts/utils/Counters.sol";

contract Vesperi is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    uint256 public maxPrice;
    uint256 public royaltyRate;

    constructor(string memory _name, string memory _symbol, uint256 _maxPrice, uint256 _royaltyRate) ERC721(_name, _symbol) {
        maxPrice = _maxPrice;
        royaltyRate = _royaltyRate; //un nombre comme 12 pour 12%
    }

    function mintNFT(address _to, string memory _tokenURI, uint256 _price) public returns (uint256) {
        require(_price <= maxPrice, "Price exceeds maximum allowed");
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();
        _safeMint(_to, newItemId);
        _setTokenURI(newItemId, _tokenURI);
        emit NFTMinted(newItemId, _to, _tokenURI, _price);
        return newItemId;
    }

    function getRoyalty(uint256 _tokenId, uint256 _price) public view returns (uint256) {
        //not done yet
        return (_price * royaltyRate) / 100;
    }

    event NFTMinted(uint256 tokenId, address indexed owner, string tokenURI, uint256 price);
}
