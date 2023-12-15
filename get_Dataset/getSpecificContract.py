import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

os.makedirs('dataSpecific', exist_ok=True)

def get_smart_contract_source_code(address):
    api_endpoint = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={api_key}"
    response = requests.get(api_endpoint)
    
    if response.status_code == 200:
        response_json = response.json()
        
        print(f"Type of response_json['result'][0]: {type(response_json['result'][0])}")
        print(f"Value of response_json['result'][0]: {response_json['result'][0]}")

        if 'result' in response_json and isinstance(response_json['result'], list) and response_json['result']:
            source_code = response_json['result'][0].get('SourceCode', 'Source code not available')
            return source_code
        else:
            print(f"Unexpected JSON structure for address {address}")
            return "Unexpected JSON structure", "Unexpected JSON structure"
    else:
        print(f"Failed to fetch data from API for address {address}")
        return "Failed to fetch data from API", "Failed to fetch data from API"


def get_smart_contract_byte_code(address):
    url = f'https://api.etherscan.io/api?module=proxy&action=eth_getCode&address={address}&tag=latest&apikey={api_key}'
    try:
        response = requests.get(url)
        data = response.json()
        bytecode = data['result']
        return bytecode
    except Exception as e:
        print(f'An error occurred: {str(e)}')

contract_address = "0x8a883a20940870dc055f2070ac8ec847ed2d9918"

victim_file_path = os.path.join('dataSpecific', f"{contract_address}.sol")
victim_file_path1 = os.path.join('dataSpecific', f"{contract_address}")
victim_bytecode_file_path = os.path.join('dataSpecific', f"{contract_address}")

def save_contract_data(contract_address):
    # victim_source_code = get_smart_contract_source_code(contract_address)
    # if victim_source_code:
    #     with open(victim_file_path,'w') as file:
    #         file.write(victim_source_code)
    #     print(f"Source code for victim contract {contract_address} saved to {victim_file_path}")

    victim_byte_code = get_smart_contract_byte_code(contract_address)
    if victim_byte_code:
        with open(victim_file_path1, 'w') as file:
            file.write(victim_byte_code)
        print(f"Source code for victim contract {contract_address} saved to {victim_file_path1}")


# contract_addresses = ["0xd1ceeeefa68a6af0a5f6046132d986066c7f9426", "0x47663541167ece0b96d9e5c60f9e470b2a20f598", "0xa62142888aba8370742be823c1782d17a0389da1",
#                       "0xd1ceeeefa68a6af0a5f6046132d986066c7f9426", "0x8a883a20940870dc055f2070ac8ec847ed2d9918", "0x29488e24cfdaa52a0b837217926c0c0853db7962",
#                       "0xab577eaed199d63af1aa8a03068d23c81fba0619", "0x5fe5b7546d1628f7348b023a0393de1fc825a4fd", "0x9f35334c9dc3c66347d33558b7cfe800380391b5",
#                       "0xd05dc25d8dad48fb9cf242d812d8fb4a653adb95"]

save_contract_data(contract_address)
