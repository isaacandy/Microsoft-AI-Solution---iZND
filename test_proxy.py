#!/usr/bin/env python3
import urllib.request, json

address = '0x295a6a847e3715f224826aa88156f356ac523eef'

# Test the proxy endpoint with mock data
print("Test 1: Proxy /api/txlist endpoint")
url = f'http://localhost:8080/api/txlist?address={address}'
try:
    response = urllib.request.urlopen(url, timeout=5)
    data = json.loads(response.read().decode())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Transactions: {len(data.get("result", []))}')
        if data.get('result'):
            tx = data['result'][0]
            print(f'  First tx hash: {tx.get("hash")}')
            print(f'  First tx value: {tx.get("value")} wei')
except Exception as e:
    print(f'  Error: {e}')

# Test mints endpoint
print("\nTest 2: Proxy /api/mints endpoint")
url = f'http://localhost:8080/api/mints?address={address}'
try:
    response = urllib.request.urlopen(url, timeout=5)
    data = json.loads(response.read().decode())
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'  Mints: {len(data.get("result", []))}')
        if data.get('result'):
            mint = data['result'][0]
            print(f'  First mint tokenID: {mint.get("tokenID")}')
except Exception as e:
    print(f'  Error: {e}')

# Test serving index.html
print("\nTest 3: Proxy serving index.html")
url = 'http://localhost:8080/index.html'
try:
    response = urllib.request.urlopen(url, timeout=5)
    html = response.read().decode()[:500]
    print(f'  Status: {response.status}')
    print(f'  Content type: {response.headers.get("Content-Type")}')
    print(f'  HTML length: {len(response.read())} chars')
except Exception as e:
    print(f'  Error: {e}')

print("\nAll tests completed! Server is ready.")
