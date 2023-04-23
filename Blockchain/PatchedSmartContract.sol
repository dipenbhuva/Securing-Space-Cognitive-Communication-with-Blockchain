pragma solidity >0.4.0;

contract data {
    struct Data {
        uint256 timestamp;
        string dataType;
        string dataHash;
        string key;
        address fromNode;
        address toNode;
    }

    mapping (uint256 => Data) private dataStore;
    mapping (address => bool) private authorized;

    function storeData(uint256 index, uint256 timestamp, string memory dataType, string memory dataHash, string memory key, address fromNode, address toNode) internal {
        require(authorized[msg.sender], "Unauthorized access");
        dataStore[index] = Data(timestamp, dataType, dataHash, key, fromNode, toNode);
    }

    function getData(uint256 index) internal view returns (uint256, string memory, string memory, string memory , address, address) {
        require(authorized[msg.sender], "Unauthorized access");
        Data memory data = dataStore[index];
        return (data.timestamp, data.dataType, data.dataHash, data.key, data.fromNode, data.toNode);
    }

    function grantAccess(address _address) internal {
        require(msg.sender == 0xD8f13e20e4b2c9fA3a26D1946584Dd07770AbF62, "Only the contract owner can grant access");
        authorized[_address] = true;
    }

    function revokeAccess(address _address) internal {
        require(msg.sender == 0xD8f13e20e4b2c9fA3a26D1946584Dd07770AbF62, "Only the contract owner can grant access");
        authorized[_address] = false;
    }

    
}
