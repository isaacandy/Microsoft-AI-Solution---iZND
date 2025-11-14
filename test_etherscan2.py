#!/usr/bin/env python3
import urllib.request, json

address = '0x295a6a847e3715f224826aa88156f356ac523eef'
apikey = 'YQ1I3BIJVRMUJ9JAC75129TP8HGI4KSATR'

# Check if this is a contract
print("Test 1: Get account balance and contract info")
url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={apikey}'
try:
    data = json.loads(urllib.request.urlopen(url, timeout=10).read())
    print(f'  Status: {data.get("status")}')
    print(f'  Result: {data.get("result")}')
except Exception as e:
    print(f'  Error: {e}')

# Try to get internal transactions
print("\nTest 2: Internal transactions")
url = f'https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&sort=desc&apikey={apikey}'
try:
    data = json.loads(urllib.request.urlopen(url, timeout=10).read())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Results: {len(data.get("result", []))}')
        if data.get('result'):
            print(f'  First: {data.get("result")[0]}')
except Exception as e:
    print(f'  Error: {e}')

# Try ERC20 transfers
print("\nTest 3: ERC20 token transfers")
url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&sort=desc&apikey={apikey}'
try:
    data = json.loads(urllib.request.urlopen(url, timeout=10).read())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Results: {len(data.get("result", []))}')
except Exception as e:
    print(f'  Error: {e}')

# Try NFT transfers
print("\nTest 4: NFT (ERC721/1155) transfers")
url = f'https://api.etherscan.io/api?module=account&action=tokennfttx&address={address}&sort=desc&apikey={apikey}'
try:
    data = json.loads(urllib.request.urlopen(url, timeout=10).read())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Results: {len(data.get("result", []))}')
        if data.get('result'):
            print(f'  First: {data.get("result")[0]}')
except Exception as e:
    print(f'  Error: {e}')

# Try Mints  
print("\nTest 5: Mint operations (tokennfttx with special filter)")
url = f'https://api.etherscan.io/api?module=account&action=tokennfttx&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={apikey}'
try:
    data = json.loads(urllib.request.urlopen(url, timeout=10).read())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Results: {len(data.get("result", []))}')
except Exception as e:
    print(f'  Error: {e}')
