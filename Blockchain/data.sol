pragma solidity >0.4.0;

contract data {
    struct Data {
        uint256 timestamp;
        string dataType;
        string dataHash;
    }

    mapping (uint256 => Data) private dataStore;
    mapping (address => bool) private authorized;

    function storeData(uint256 index, uint256 timestamp, string memory dataType, string memory dataHash) public {
        require(authorized[msg.sender], "Unauthorized access");
        dataStore[index] = Data(timestamp, dataType, dataHash);
    }

    function getData(uint256 index) public view returns (uint256, string memory, string memory) {
        require(authorized[msg.sender], "Unauthorized access");
        Data memory data = dataStore[index];
        return (data.timestamp, data.dataType, data.dataHash);
    }

    function grantAccess(address _address) public {
    require(msg.sender == 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4, "Only the contract owner can grant access");
        authorized[_address] = true;
    }

    function revokeAccess(address _address) public {
    require(msg.sender == 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4, "Only the contract owner can grant access");
        authorized[_address] = false;
    }
}