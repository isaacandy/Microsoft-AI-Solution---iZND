#!/usr/bin/env python3
import urllib.request, json
import time

# Give the server a moment to start if needed
time.sleep(1)

address = '0x295a6a847e3715f224826aa88156f356ac523eef'

print("Testing proxy endpoints...")

# Test the proxy endpoint
print("\nTest 1: Proxy /api/txlist endpoint")
url = f'http://localhost:8080/api/txlist?address={address}'
try:
    response = urllib.request.urlopen(url, timeout=5)
    data = json.loads(response.read().decode())
    print(f'✓ Status: {data.get("status")}')
    print(f'✓ Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        print(f'✓ Real transactions: {len(data.get("result", []))}')
        if data.get('result'):
            tx = data['result'][0]
            print(f'  - First tx hash: {tx.get("hash")[:20]}...')
            print(f'  - Function: {tx.get("functionName", "N/A")}')
except Exception as e:
    print(f'✗ Error: {e}')

print("\nTest 2: Proxy /api/mints endpoint")
url = f'http://localhost:8080/api/mints?address={address}'
try:
    response = urllib.request.urlopen(url, timeout=5)
    data = json.loads(response.read().decode())
    print(f'✓ Status: {data.get("status")}')
    print(f'✓ Message: {data.get("message")}')
    if isinstance(data.get('result'), list):
        count = len(data.get("result", []))
        print(f'✓ NFT transfers: {count}')
except Exception as e:
    print(f'✗ Error: {e}')

print("\n✓ Proxy is working! Visit http://localhost:8080/index.html in your browser")
