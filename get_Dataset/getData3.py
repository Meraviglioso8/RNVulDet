import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

# Replace 'yourfile.json' with your JSON file's name
file_path = '../dataset/dataset_3_suspicious_transactions.json'

# Open the JSON file and load its contents into a Python variable
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Ensure the 'data' directory exists
os.makedirs('data3', exist_ok=True)

# [Your functions for fetching smart contract source code and bytecode remain the same]
def get_smart_contract_source_code(address):
    api_endpoint = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={api_key}"
    response = requests.get(api_endpoint)
    
    if response.status_code == 200:
        response_json = response.json()
        
        # Debugging: Print the type and value of response_json['result'][0]
        print(f"Type of response_json['result'][0]: {type(response_json['result'][0])}")
        print(f"Value of response_json['result'][0]: {response_json['result'][0]}")

        # Check if the 'result' key is in the response and is a list
        if 'result' in response_json and isinstance(response_json['result'], list) and response_json['result']:
            # Assuming 'result' is a list of dictionaries
            source_code = response_json['result'][0].get('SourceCode', 'Source code not available')
            return source_code
        else:
            print(f"Unexpected JSON structure for address {address}")
            return "Unexpected JSON structure", "Unexpected JSON structure"
    else:
        print(f"Failed to fetch data from API for address {address}")
        return "Failed to fetch data from API", "Failed to fetch data from API"


def get_smart_contract_byte_code(address):
# Etherscan API URL
    url = f'https://api.etherscan.io/api?module=proxy&action=eth_getCode&address={address}&tag=latest&apikey={api_key}'
    try:
    # Send a GET request to the Etherscan API
        response = requests.get(url)
        # Parse the JSON response
        data = response.json()
        # Get the bytecode
        bytecode = data['result']
        return bytecode
    except Exception as e:
        print(f'An error occurred: {str(e)}')
# Loop through each item in json_data
# get victim
for item in json_data:
    # Extract the victim contract address
    victim_address = item['potential_victim_contract']

    # Define file paths for the victim contract
    victim_file_path = os.path.join('data3', f"{victim_address}.sol")
    victim_bytecode_file_path = os.path.join('data3', f"{victim_address}")

    # Check if the source code file already exists
    if not os.path.exists(victim_file_path):
        victim_source_code = get_smart_contract_source_code(victim_address)
        if victim_source_code:
            with open(victim_file_path, 'w') as file:
                file.write(victim_source_code)
            print(f"Source code for victim contract {victim_address} saved to {victim_file_path}")
    else:
        print(f"Source code file for victim contract {victim_address} already exists.")

    # Check if the bytecode file already exists
    if not os.path.exists(victim_bytecode_file_path):
        victim_bytecode = get_smart_contract_byte_code(victim_address)
        if victim_bytecode:
            with open(victim_bytecode_file_path, 'w') as file:
                file.write(victim_bytecode)
            print(f"Bytecode for victim contract {victim_address} saved to {victim_bytecode_file_path}")
    else:
        print(f"Bytecode file for victim contract {victim_address} already exists.")

    # Optionally, process potential malicious contracts in a similar way
    # for malicious_address in item['potential_malicious_contracts']:
    #     [Repeat the process for each malicious contract, with the same existence checks]

# Attack contract
# # Loop through each item in json_data
# for item in json_data:
#     # Loop through each potential malicious contract address
#     for malicious_address in item['potential_malicious_contracts']:
#         # Process the malicious contract
#         malicious_source_code = get_smart_contract_source_code(malicious_address)
#         malicious_bytecode = get_smart_contract_byte_code(malicious_address)

#         # Save the malicious contract source code
#         if malicious_source_code:
#             malicious_file_path = os.path.join('data3', f"{malicious_address}.sol")
#             with open(malicious_file_path, 'w') as file:
#                 file.write(malicious_source_code)
#             print(f"Source code for malicious contract {malicious_address} saved to {malicious_file_path}")

#         # Save the malicious contract bytecode
#         if malicious_bytecode:
#             malicious_bytecode_file_path = os.path.join('data3', f"{malicious_address}")
#             with open(malicious_bytecode_file_path, 'w') as file:
#                 file.write(malicious_bytecode)
#             print(f"Bytecode for malicious contract {malicious_address} saved to {malicious_bytecode_file_path}")

