#!/usr/bin/env python3
"""
Simple Python proxy server for Etherscan API V2.
Serves static files and forwards /api/* requests to Etherscan.
Usage: python proxy.py
"""

import os
import sys
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Get Etherscan API key from environment or .env file
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', '').strip()
# Get provider URL for JSON-RPC (Infura/Alchemy) from .env
PROVIDER_URL = os.getenv('PROVIDER_URL', '').strip()

# Try to load from .env file if not in environment
if not ETHERSCAN_API_KEY:
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, val = line.split('=', 1)
                    if key.strip() == 'ETHERSCAN_API_KEY':
                        ETHERSCAN_API_KEY = val.strip()
                        break

# Try to read PROVIDER_URL from .env as well if not set in environment
if not PROVIDER_URL:
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, val = line.split('=', 1)
                    if key.strip() == 'PROVIDER_URL':
                        PROVIDER_URL = val.strip()
                        break

# If PORT not provided via environment, read it from .env so local .env can control server port
if not os.getenv('PORT'):
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                if key.strip() == 'PORT':
                    try:
                        PORT = int(val.strip())
                    except Exception:
                        pass
                    break

if not ETHERSCAN_API_KEY:
    print('Warning: ETHERSCAN_API_KEY not set. Set it in a .env file or environment variable.')
else:
    print(f'Etherscan API Key loaded: {ETHERSCAN_API_KEY[:10]}...')

# Use 8080 by default (port 3000 often has permission issues on Windows)
PORT = int(os.getenv('PORT', '8080'))
BASE_DIR = Path(__file__).parent


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests: proxy /api/* to Etherscan, serve static files for others."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parsed_path.query

        print(f'Request: {self.path}')

        # Handle API routes
        if path.startswith('/api/txlist'):
            print(f'Routing to txlist handler')
            return self.handle_txlist(query)
        elif path.startswith('/api/mints'):
            print(f'Routing to mints handler')
            return self.handle_mints(query)
        elif path.startswith('/api/logs'):
            print(f'Routing to logs handler')
            return self.handle_logs(query)

        # Serve static files or fallback to index.html
        if path == '/' or path.endswith('.html') or path.endswith('.css') or path.endswith('.js') or path.endswith('.ico'):
            return self.serve_static_file(path)

        # Default: serve index.html for non-API paths
        return self.serve_static_file('/index.html')

    # Note: mock data removed. Proxy now returns live V2 responses or clear errors.

    def handle_txlist(self, query):
        """Proxy /api/txlist to Etherscan V2 transactions endpoint, with fallback to mock data."""
        try:
            params = parse_qs(query)
            address = params.get('address', [None])[0]

            if not address:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'address query parameter required'}).encode())
                return

            # Use V2 API with proper chainid parameter (chainid=1 for Ethereum mainnet)
            url_v2 = f'https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}'
            
            print(f'Calling Etherscan V2: {url_v2[:100]}...')
            try:
                request = urllib.request.Request(url_v2)
                response = urllib.request.urlopen(request, timeout=15)
                data = response.read()
                data_str = data.decode('utf-8')
                print(f'V2 response length: {len(data_str)} bytes')
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                print(f'Response sent successfully')
                return
            except urllib.error.HTTPError as e:
                # Forward Etherscan HTTP error details to client
                try:
                    error_body = e.read().decode('utf-8', errors='ignore')
                except Exception:
                    error_body = ''
                print(f'Etherscan HTTP error: {e.code} {e.reason}. Body: {error_body[:300]}')
                self.send_response(502)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                payload = {'error': 'Etherscan HTTP error', 'code': e.code, 'reason': str(e.reason), 'body': error_body}
                self.wfile.write(json.dumps(payload).encode())
                return
                
        except Exception as e:
            print(f'Proxy error: {e}')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            payload = {'error': 'proxy_exception', 'message': str(e)}
            self.wfile.write(json.dumps(payload).encode())

    def handle_logs(self, query):
        """Proxy /api/logs to a JSON-RPC provider (Infura/Alchemy) and return parsed Transfer logs.
        Requires PROVIDER_URL to be set in environment or .env.
        """
        try:
            params = parse_qs(query)
            address = params.get('address', [None])[0]
            from_block = params.get('fromBlock', ['0'])[0]
            to_block = params.get('toBlock', ['latest'])[0]

            if not address:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'address query parameter required'}).encode())
                return

            if not PROVIDER_URL:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'PROVIDER_URL not configured. Set PROVIDER_URL in .env or env.'}).encode())
                return

            # ERC-721 Transfer event topic
            topic0 = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

            rpc_payload = {
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'eth_getLogs',
                'params': [{
                    'fromBlock': '0x' + format(int(from_block) if from_block.isdigit() else 0, 'x') if from_block != 'latest' else '0x0',
                    'toBlock': to_block if to_block == 'latest' else '0x' + format(int(to_block), 'x'),
                    'address': address,
                    'topics': [topic0]
                }]
            }

            req = urllib.request.Request(PROVIDER_URL, data=json.dumps(rpc_payload).encode(), headers={'Content-Type': 'application/json'})
            try:
                resp = urllib.request.urlopen(req, timeout=30)
                body = resp.read().decode('utf-8')
                data = json.loads(body)
                logs = data.get('result', [])

                parsed = []
                for log in logs:
                    # topics: [topic0, from, to, tokenId]
                    topics = log.get('topics', [])
                    token_id = None
                    from_addr = None
                    to_addr = None
                    if len(topics) >= 4:
                        from_addr = '0x' + topics[1][-40:]
                        to_addr = '0x' + topics[2][-40:]
                        token_id = int(topics[3], 16)
                    else:
                        # fallback: token id in data
                        data_hex = log.get('data', '')
                        try:
                            token_id = int(data_hex, 16) if data_hex else None
                        except Exception:
                            token_id = None

                    parsed.append({
                        'blockNumber': int(log.get('blockNumber', '0'), 16) if isinstance(log.get('blockNumber', None), str) else log.get('blockNumber'),
                        'transactionHash': log.get('transactionHash'),
                        'from': from_addr,
                        'to': to_addr,
                        'tokenId': token_id,
                        'logIndex': int(log.get('logIndex', '0'), 16) if isinstance(log.get('logIndex', None), str) else log.get('logIndex')
                    })

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': '1', 'message': 'OK', 'result': parsed}).encode())
                return
            except urllib.error.HTTPError as e:
                try:
                    error_body = e.read().decode('utf-8', errors='ignore')
                except Exception:
                    error_body = ''
                self.send_response(502)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'provider_http_error', 'code': e.code, 'body': error_body}).encode())
                return

        except Exception as e:
            print(f'Logs proxy error: {e}')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'proxy_exception', 'message': str(e)}).encode())

    # Note: mock mints removed. Proxy now returns live V2 responses or clear errors.

    def handle_mints(self, query):
        """Proxy /api/mints to Etherscan V2 ERC-721 transfers endpoint, with fallback to mock data."""
        try:
            params = parse_qs(query)
            address = params.get('address', [None])[0]
            page = params.get('page', ['1'])[0]
            offset = params.get('offset', ['100'])[0]

            if not address:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'address query parameter required'}).encode())
                return

            # Use V2 API with proper chainid parameter (chainid=1 for Ethereum mainnet)
            url_v2 = f'https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokennfttx&address={address}&page={page}&offset={offset}&sort=desc&apikey={ETHERSCAN_API_KEY}'
            
            print(f'Calling Etherscan V2: {url_v2[:100]}...')
            try:
                request = urllib.request.Request(url_v2)
                response = urllib.request.urlopen(request, timeout=15)
                data = response.read()
                data_str = data.decode('utf-8')
                print(f'V2 response length: {len(data_str)} bytes')
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                print(f'Response sent successfully')
                return
            except urllib.error.HTTPError as e:
                try:
                    error_body = e.read().decode('utf-8', errors='ignore')
                except Exception:
                    error_body = ''
                print(f'Etherscan HTTP error: {e.code} {e.reason}. Body: {error_body[:300]}')
                self.send_response(502)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                payload = {'error': 'Etherscan HTTP error', 'code': e.code, 'reason': str(e.reason), 'body': error_body}
                self.wfile.write(json.dumps(payload).encode())
                return
                
        except Exception as e:
            print(f'Proxy error: {e}')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            payload = {'error': 'proxy_exception', 'message': str(e)}
            self.wfile.write(json.dumps(payload).encode())

    def serve_static_file(self, file_path):
        """Serve static files from the base directory."""
        if file_path.startswith('/'):
            file_path = file_path[1:]

        full_path = BASE_DIR / file_path
        if not full_path.exists() or not full_path.is_file():
            # Fallback to index.html if file not found
            full_path = BASE_DIR / 'index.html'

        try:
            content = full_path.read_bytes()
            content_type = self.guess_content_type(str(full_path))

            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))

    def guess_content_type(self, file_path):
        """Guess content type based on file extension."""
        if file_path.endswith('.html'):
            return 'text/html; charset=utf-8'
        elif file_path.endswith('.css'):
            return 'text/css'
        elif file_path.endswith('.js'):
            return 'application/javascript'
        elif file_path.endswith('.json'):
            return 'application/json'
        elif file_path.endswith('.ico'):
            return 'image/x-icon'
        elif file_path.endswith('.png'):
            return 'image/png'
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            return 'image/jpeg'
        elif file_path.endswith('.gif'):
            return 'image/gif'
        else:
            return 'application/octet-stream'

    def log_message(self, format, *args):
        """Log requests to console."""
        print(f'[{self.client_address[0]}] {format % args}')


if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), ProxyHandler)
    print(f'Server running on http://localhost:{PORT}')
    print(f'Open the site at: http://localhost:{PORT}/index.html')
    print(f'Press Ctrl+C to stop.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
        sys.exit(0)
