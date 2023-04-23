pragma solidity >0.4.25;

contract Bank
{
    uint256 public bal = 10;
    uint256 public balance = 100;

    
    function getBalance() view public returns(uint256)
    {

        return bal;
       
    }

    function withdraw(uint256 amt) public
    {
        bal = bal - amt;

    }

     function deposit(uint256 amt) public
    {
        bal = bal + amt;

    }

    function sayHello() view public returns(string memory newName)
    {
    newName = "hello";
    }
}