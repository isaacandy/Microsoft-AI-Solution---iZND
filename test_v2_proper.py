#!/usr/bin/env python3
import urllib.request, json

address = '0x295a6a847e3715f224826aa88156f356ac523eef'
apikey = 'YQ1I3BIJVRMUJ9JAC75129TP8HGI4KSATR'

# Test V2 API with proper chainid parameter
print("Test 1: Etherscan V2 API with chainid=1 (txlist)")
url = f'https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist&address={address}&sort=desc&apikey={apikey}'
print(f"URL: {url}")
try:
    response = urllib.request.urlopen(url, timeout=10)
    data = json.loads(response.read().decode())
    print(f'  Status code: {response.status}')
    print(f'  Response status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Transactions found: {len(data.get("result", []))}')
        if data.get('result'):
            print(f'  First tx: {data["result"][0]}')
    else:
        print(f'  Result type: {type(data.get("result"))}')
        print(f'  Result: {data.get("result")}')
except Exception as e:
    print(f'  Error: {e}')

# Test NFT transfers
print("\n\nTest 2: Etherscan V2 API with chainid=1 (tokennfttx)")
url = f'https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokennfttx&address={address}&sort=desc&apikey={apikey}'
print(f"URL: {url}")
try:
    response = urllib.request.urlopen(url, timeout=10)
    data = json.loads(response.read().decode())
    print(f'  Status code: {response.status}')
    print(f'  Response status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  NFT transfers found: {len(data.get("result", []))}')
        if data.get('result'):
            print(f'  First transfer: {data["result"][0]}')
    else:
        print(f'  Result type: {type(data.get("result"))}')
        print(f'  Result: {data.get("result")}')
except Exception as e:
    print(f'  Error: {e}')
