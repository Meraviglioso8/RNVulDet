import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

# Replace 'yourfile.json' with your JSON file's name
file_path = './dataset/dataset_2_popular_contracts.json'

# Open the JSON file and load its contents into a Python variable
with open(file_path, 'r') as file:
    contract_addresses = json.load(file)

# Ensure the 'data' directory exists
os.makedirs('data2', exist_ok=True)

# [Rest of your functions remain the same]
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
# Loop through each contract address in the list
for address in contract_addresses:
    source_code = get_smart_contract_source_code(address)
    bytecode = get_smart_contract_byte_code(address)

    # If source code was found, write it to a .sol file
    if source_code:
        file_path = os.path.join('data2', f"{address}.sol")
        with open(file_path, 'w') as file:
            file.write(source_code)
        print(f"Source code for {address} saved to {file_path}")
    
    # If bytecode was found, write it to a .bytecode file
    if bytecode:
        bytecode_file_path = os.path.join('data2', f"{address}")
        with open(bytecode_file_path, 'w') as file:
            file.write(bytecode)
        print(f"Bytecode for {address} saved to {bytecode_file_path}")
