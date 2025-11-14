#!/usr/bin/env python3
import urllib.request, json

address = '0x295a6a847e3715f224826aa88156f356ac523eef'
apikey = 'YQ1I3BIJVRMUJ9JAC75129TP8HGI4KSATR'

# Try Etherscan V2 API format
print("Test 1: Etherscan V2 API - Account transactions")
url = f'https://api.etherscan.io/api/v2/account/transactions?address={address}&sort=desc&apikey={apikey}'
try:
    response = urllib.request.urlopen(url, timeout=10)
    print(f'  Status code: {response.status}')
    data = json.loads(response.read())
    print(f'  Response type: {type(data)}')
    if isinstance(data, list):
        print(f'  Transactions: {len(data)}')
        if data:
            print(f'  First tx keys: {list(data[0].keys())}')
    elif isinstance(data, dict):
        print(f'  Keys: {list(data.keys())}')
        if 'result' in data:
            print(f'  Result type: {type(data["result"])}')
except Exception as e:
    print(f'  Error: {e}')

# Try V2 with mints  
print("\nTest 2: Etherscan V2 API - Account token transfers (NFT mints)")
url = f'https://api.etherscan.io/api/v2/account/nft-transfers?address={address}&sort=desc&apikey={apikey}'
try:
    response = urllib.request.urlopen(url, timeout=10)
    print(f'  Status code: {response.status}')
    data = json.loads(response.read())
    print(f'  Response type: {type(data)}')
    if isinstance(data, list):
        print(f'  NFT transfers: {len(data)}')
        if data:
            print(f'  First transfer keys: {list(data[0].keys())}')
    elif isinstance(data, dict):
        print(f'  Keys: {list(data.keys())}')
except Exception as e:
    print(f'  Error: {e}')

# Try internal transactions V2
print("\nTest 3: Etherscan V2 API - Internal transactions")
url = f'https://api.etherscan.io/api/v2/account/internal-transactions?address={address}&sort=desc&apikey={apikey}'
try:
    response = urllib.request.urlopen(url, timeout=10)
    print(f'  Status code: {response.status}')
    data = json.loads(response.read())
    if isinstance(data, list):
        print(f'  Internal txs: {len(data)}')
    elif isinstance(data, dict):
        print(f'  Response keys: {list(data.keys())}')
except Exception as e:
    print(f'  Error: {e}')
