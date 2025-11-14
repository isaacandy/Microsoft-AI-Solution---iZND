#!/usr/bin/env python3
import urllib.request, json, urllib.error

address = '0x295a6a847e3715f224826aa88156f356ac523eef'
apikey = 'YQ1I3BIJVRMUJ9JAC75129TP8HGI4KSATR'

# Test a simple balance check
print("Test 1: Get balance with different endpoints")
endpoints = [
    f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest',
    f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={apikey}',
]

for endpoint in endpoints:
    print(f"\n  URL: {endpoint[:100]}...")
    try:
        response = urllib.request.urlopen(endpoint, timeout=10)
        data = json.loads(response.read().decode())
        print(f'  Status: {data.get("status")}')
        print(f'  Result: {data.get("result")[:50] if data.get("result") else "None"}...')
        if 'message' in data:
            print(f'  Message: {data.get("message")}')
    except urllib.error.HTTPError as e:
        print(f'  HTTP Error {e.code}: {e.reason}')
        try:
            error_data = json.loads(e.read().decode())
            print(f'  Error response: {error_data}')
        except:
            print(f'  Error body could not be parsed')
    except Exception as e:
        print(f'  Error: {e}')

# Check if this address has any ETH
print("\n\nTest 2: Check if address holds ETH")
url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest'
try:
    response = urllib.request.urlopen(url, timeout=10)
    data = json.loads(response.read().decode())
    if data.get('status') == '1':
        balance_wei = int(data.get('result', 0))
        balance_eth = balance_wei / 1e18
        print(f'  Balance: {balance_eth} ETH')
    else:
        print(f'  Status: {data.get("status")}')
        print(f'  Result: {data.get("result")}')
except Exception as e:
    print(f'  Error: {e}')

# Try to get the account type (contract or EOA)
print("\nTest 3: Try simple ethers.js style provider query simulation")
print("  Note: This address may need to be queried via blockscout or other explorer")
print(f"  URL to check manually: https://etherscan.io/address/{address}")
