#!/usr/bin/env python3
"""
Minimal Python proxy server for Etherscan V2 API and JSON-RPC provider.
Serves static files and proxies /api/* requests.
Usage: python proxy.py
Environment variables: ETHERSCAN_API_KEY, PROVIDER_URL, PORT=8080
"""

import os
import sys
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Load environment variables from .env file if present
def load_env_file():
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip())

load_env_file()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', '').strip()
PROVIDER_URL = os.getenv('PROVIDER_URL', '').strip()
PORT = int(os.getenv('PORT', '8080'))
BASE_DIR = Path(__file__).parent

if ETHERSCAN_API_KEY:
    print(f'✓ Etherscan API Key loaded: {ETHERSCAN_API_KEY[:10]}...')
else:
    print('⚠ Warning: ETHERSCAN_API_KEY not set. Set it in .env file or environment.')

if PROVIDER_URL:
    print(f'✓ Provider URL loaded.')
else:
    print('⚠ Warning: PROVIDER_URL not set. /api/logs will not work.')


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parsed_path.query

        if path.startswith('/api/txlist'):
            return self.handle_txlist(query)
        elif path.startswith('/api/mints'):
            return self.handle_mints(query)
        elif path.startswith('/api/logs'):
            return self.handle_logs(query)

        # Serve static files
        return self.serve_static_file(path if path != '/' else '/index.html')

    def handle_txlist(self, query):
        """Proxy /api/txlist to Etherscan V2 txlist endpoint."""
        try:
            params = parse_qs(query)
            address = params.get('address', [None])[0]

            if not address:
                self.send_json(400, {'error': 'address parameter required'})
                return

            url = f'https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}'
            
            try:
                response = urllib.request.urlopen(urllib.request.Request(url), timeout=15)
                data = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8', errors='ignore')
                self.send_json(502, {'error': 'Etherscan error', 'code': e.code})
                
        except Exception as e:
            print(f'Error in handle_txlist: {e}')
            self.send_json(500, {'error': str(e)})

    def handle_mints(self, query):
        """Proxy /api/mints to Etherscan V2 tokennfttx endpoint."""
        try:
            params = parse_qs(query)
            address = params.get('address', [None])[0]
            page = params.get('page', ['1'])[0]
            offset = params.get('offset', ['100'])[0]

            if not address:
                self.send_json(400, {'error': 'address parameter required'})
                return

            url = f'https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokennfttx&address={address}&page={page}&offset={offset}&sort=desc&apikey={ETHERSCAN_API_KEY}'
            
            try:
                response = urllib.request.urlopen(urllib.request.Request(url), timeout=15)
                data = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
            except urllib.error.HTTPError as e:
                self.send_json(502, {'error': 'Etherscan error', 'code': e.code})
                
        except Exception as e:
            print(f'Error in handle_mints: {e}')
            self.send_json(500, {'error': str(e)})

    def handle_logs(self, query):
        """Proxy /api/logs to JSON-RPC provider for eth_getLogs (ERC-721 Transfer events)."""
        try:
            params = parse_qs(query)
            address = params.get('address', [None])[0]
            from_block = params.get('fromBlock', ['0'])[0]
            to_block = params.get('toBlock', ['latest'])[0]

            if not address:
                self.send_json(400, {'error': 'address parameter required'})
                return

            if not PROVIDER_URL:
                self.send_json(400, {'error': 'PROVIDER_URL not configured'})
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
                    topics = log.get('topics', [])
                    token_id = None
                    from_addr = None
                    to_addr = None
                    if len(topics) >= 4:
                        from_addr = '0x' + topics[1][-40:]
                        to_addr = '0x' + topics[2][-40:]
                        token_id = int(topics[3], 16)

                    parsed.append({
                        'blockNumber': int(log.get('blockNumber', '0'), 16) if isinstance(log.get('blockNumber'), str) else log.get('blockNumber'),
                        'transactionHash': log.get('transactionHash'),
                        'from': from_addr,
                        'to': to_addr,
                        'tokenId': token_id,
                        'logIndex': int(log.get('logIndex', '0'), 16) if isinstance(log.get('logIndex'), str) else log.get('logIndex')
                    })

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': '1', 'message': 'OK', 'result': parsed}).encode())
            except urllib.error.HTTPError as e:
                self.send_json(502, {'error': 'Provider error', 'code': e.code})

        except Exception as e:
            print(f'Error in handle_logs: {e}')
            self.send_json(500, {'error': str(e)})

    def serve_static_file(self, file_path):
        """Serve static files from base directory."""
        if file_path.startswith('/'):
            file_path = file_path[1:]

        full_path = BASE_DIR / file_path
        if not full_path.exists() or not full_path.is_file():
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
            self.send_json(500, {'error': str(e)})

    def guess_content_type(self, file_path):
        """Guess content type based on file extension."""
        ext = Path(file_path).suffix
        types = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.ico': 'image/x-icon',
        }
        return types.get(ext, 'application/octet-stream')

    def send_json(self, status_code, payload):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def log_message(self, format, *args):
        """Suppress verbose logging."""
        pass


if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), ProxyHandler)
    print(f'\n🚀 Server running on http://localhost:{PORT}')
    print(f'📂 Serving files from: {BASE_DIR}')
    print(f'🌐 Open http://localhost:{PORT}/index.html')
    print(f'⏸  Press Ctrl+C to stop.\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n✓ Server stopped.')
        sys.exit(0)
