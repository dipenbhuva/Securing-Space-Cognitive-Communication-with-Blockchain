import os
import re
from solc import compile_files, link_code
from web3 import Web3

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

def load_smart_contract(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def detect_vulnerabilities(contract_code):
    vulnerabilities = []
    
    # Detect reentrancy vulnerabilities
    if re.search(r'\.call\(', contract_code):
        vulnerabilities.append('reentrancy')

    # Detect integer overflow vulnerabilities
    if re.search(r'\+\+|-\-', contract_code):
        vulnerabilities.append('integer_overflow')

    # Detect improper access control vulnerabilities
    if re.search(r'public', contract_code):
        vulnerabilities.append('improper_access_control')

    return vulnerabilities

def generate_patch(vulnerability, contract_code):
    patched_code = contract_code

    if vulnerability == 'reentrancy':
        patched_code = re.sub(r'\.call\(', '.transfer(', patched_code)
    
    if vulnerability == 'integer_overflow':
        patched_code = re.sub(r'(\+\+|-\-)', r'SafeMath.\1', patched_code)
    
    if vulnerability == 'improper_access_control':
        patched_code = re.sub(r'public', 'internal', patched_code)

    return patched_code

def main():
    contract_file_path = 'datav2.sol'
    contract_code = load_smart_contract(contract_file_path)
    vulnerabilities = detect_vulnerabilities(contract_code)

    if vulnerabilities:
        print(f'Vulnerabilities detected: {", ".join(vulnerabilities)}')
        patched_code = contract_code

        for vulnerability in vulnerabilities:
            patched_code = generate_patch(vulnerability, patched_code)

        with open('PatchedSmartContract.sol', 'w') as f:
            f.write(patched_code)

        print('Patched smart contract saved as PatchedSmartContract.sol')
    else:
        print('No vulnerabilities detected.')

if __name__ == '__main__':
    main()
