from web3 import Web3, HTTPProvider
import json
from solcx import compile_source
import timeit
import time
from cryptography.fernet import Fernet
import numpy as np
import pandas
import os
import sys


# Connect to the blockchain network
w3 = Web3(Web3.HTTPProvider('http://172.20.41.77:7545'))
w3.is_connected()
w3.eth.default_account = w3.eth.accounts[0]

# Load and compile the Solidity contract

# Deploy the contract

abi = '[{"inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}], "name": "getData", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "string", "name": "", "type": "string"}, {"internalType": "string", "name": "", "type": "string"}, {"internalType": "string", "name": "", "type": "string"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}], "name": "grantAccess", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}], "name": "revokeAccess", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}, {"internalType": "uint256", "name": "timestamp", "type": "uint256"}, {"internalType": "string", "name": "dataType", "type": "string"}, {"internalType": "string", "name": "dataHash", "type": "string"}, {"internalType": "string", "name": "key", "type": "string"}, {"internalType": "address", "name": "fromNode", "type": "address"}, {"internalType": "address", "name": "toNode", "type": "address"}], "name": "storeData", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'

contract_address = '0x4E6AeE5E37D48a2593f5baFE880B14C318502ebe'

data = w3.eth.contract(address = contract_address,abi=abi)
#print(Bank)

#transcation_Hash = data.constructor().transact()
#print(transcation_Hash)

#transcation_receipt = w3.eth.wait_for_transaction_receipt(transcation_Hash)
#print(transcation_receipt)

##Calling Function To Print Values

#data = w3.eth.contract(address = transcation_receipt.contractAddress, abi=abi)
# Define a class to encapsulate the data
def generate_key():
    return Fernet.generate_key()

def encrypt_data(plaintext, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(plaintext.encode())

def decrypt_data(ciphertext, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(ciphertext).decode()

class Data:
    def __init__(self, index, data_type, data_hash):
        self.index = index
        self.timestamp = int(time.time())
        self.data_type = data_type
        self.data = data_hash
        self.from_node = w3.eth.default_account
        self.to_node = w3.eth.accounts[1]
        self.key = str(key)
    
    def store(self):
        
        # Send a transaction to the blockchain to store the data
        data = w3.eth.contract(address = contract_address, abi=abi)
        deposit_Hash = data.functions.storeData(self.index, self.timestamp, self.data_type, self.data, self.key, self.from_node, self.to_node).transact()
        #print(deposit_Hash)
        deposit_receipt = w3.eth.wait_for_transaction_receipt(deposit_Hash)
        print(deposit_receipt)

    def retrieve(self, index):
        # Call the blockchain to retrieve the data

        data = w3.eth.contract(address = contract_address,abi=abi)
        print(data.functions.getData(index).call())
        return data.functions.getData(index).call()
    
        
data_df = pandas.read_excel('InSitu.xlsx', sheet_name='Sheet1')

#print(data_df.head())   
    
# Create an instance of the Data class and grant access the data transcation on the blockchain
data = w3.eth.contract(abi=abi, address = contract_address)
deposit_Hash = data.functions.grantAccess('0xC289FDa547493dA5D862c812f9B1E1C427681077').transact()
#print(deposit_Hash)
#deposit_receipt = w3.eth.wait_for_transaction_receipt(deposit_Hash)
key = generate_key()
for i in data_df.iterrows():
	a = 0
	tic=timeit.default_timer()
	demostring = str(i)
	# Encrypt data before storing it on the blockchain
	encrypted_data = encrypt_data(demostring, key)
	cc = str(encrypted_data)
	#x = encrypted_data.replace("'","")
	# Create an instance of the Data class and store the encrypted data on the blockchain
	data = Data(a, 'string', cc)
	data.store()
	toc=timeit.default_timer()
	
	old_stdout = sys.stdout
	log_file = open("message_send.log","a")
	sys.stdout = log_file
	print(toc - tic)
	sys.stdout = old_stdout
	log_file.close()
	#retrieved_data = np.array(6)
	# Retrieve the data from the blockchain and decrypt it
	tic_rec=timeit.default_timer()
	retrieved_data = data.retrieve(a)
	toc_rec=timeit.default_timer()
	#decrypted_data = decrypt_data(retrieved_data[2], retrieved_data[3])
	old_stdout = sys.stdout
	log_file = open("message_receive.log","a")
	sys.stdout = log_file
	print(toc_rec - tic_rec)
	sys.stdout = old_stdout
	log_file.close()
	a=a+1


	

# Retrieve the data from the blockchain and print it
#retrieved_data = data.retrieve(4)

