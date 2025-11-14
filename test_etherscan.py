#!/usr/bin/env python3
import urllib.request, json

address = '0x295a6a847e3715f224826aa88156f356ac523eef'

# Test 1: Without API key
print("Test 1: Without API key")
url1 = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc'
try:
    data = json.loads(urllib.request.urlopen(url1, timeout=10).read())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Transactions: {len(data.get("result", []))}')
except Exception as e:
    print(f'  Error: {e}')

# Test 2: With API key
print("\nTest 2: With API key")
url2 = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey=YQ1I3BIJVRMUJ9JAC75129TP8HGI4KSATR'
try:
    data = json.loads(urllib.request.urlopen(url2, timeout=10).read())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Transactions: {len(data.get("result", []))}')
except Exception as e:
    print(f'  Error: {e}')

# Test 3: Token transfers without API key
print("\nTest 3: Token transfers (ERC-20/721) without API key")
url3 = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&sort=desc'
try:
    data = json.loads(urllib.request.urlopen(url3, timeout=10).read())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Transfers: {len(data.get("result", []))}')
except Exception as e:
    print(f'  Error: {e}')
