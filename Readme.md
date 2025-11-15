# Web3 AI Solutions | iZND Group

Live blockchain transactions and NFT mints for **TheAlien.888** on Ethereum.

---

## 🚀 Quick Start
# Web3 AI Solutions | iZND Group

Live blockchain transactions and NFT mints for **TheAlien.888** on Ethereum.

---

## 🚀 How to load this portal (local development)

This project serves a static frontend (`index.html`) and a small Python proxy (`proxy.py`) that talks to Etherscan V2 and an optional JSON-RPC provider (Infura/Alchemy). The proxy keeps your API keys server-side and sets CORS headers so the browser can fetch live data.

Prerequisites:
- Python 3.8+ installed
- An Etherscan V2 API key
- (Optional) An Infura/Alchemy JSON-RPC URL for `eth_getLogs` fallback

### 1) Create `.env` in project root
Create a `.env` file with your keys and desired proxy port. Example:

```ini
ETHERSCAN_API_KEY=your_etherscan_v2_api_key
PROVIDER_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
PORT=9090
```

Notes:
- `PORT` controls the proxy server only (the Python proxy reads this variable). Default in the repository examples is `9090`.

### 2) Start the proxy (keeps API keys secret)
Run the proxy from the project root:

```bash
python proxy.py
```

You should see output similar to:

```
✓ Etherscan API Key loaded: YQ1I3BIJVR...
✓ Provider URL loaded.

🚀 Server running on http://localhost:9090
📂 Serving files from: <project root>
```

### 3) Serve the static frontend
The frontend is plain HTML/CSS/JS. You can serve it with Python's simple HTTP server (or your preferred static host):

```bash
# from project root
python -m http.server 8000
# then open http://localhost:8000 in your browser
```

The page's JavaScript detects `localhost` and will call the proxy at the port you set in `.env` (e.g. `http://localhost:9090`).

---

## 🌐 Local API endpoints (proxy)

The proxy exposes the following endpoints (examples):

```text
GET http://localhost:9090/api/txlist?address=<contract_address>
		# Returns a list of transactions for the address (Etherscan V2 response)

GET http://localhost:9090/api/mints?address=<contract_address>&page=1&offset=100
		# Returns NFT transfer history (Etherscan tokennfttx)

GET http://localhost:9090/api/logs?address=<contract_address>&fromBlock=0&toBlock=latest
		# Calls JSON-RPC eth_getLogs to extract Transfer events (used as a fallback)
```

Notes:
- The proxy sets `Access-Control-Allow-Origin: *` so your frontend can fetch data without CORS errors.
- If you change `PORT` in `.env`, update any deployment scripts that expect the proxy on a different port.

---

## 🔁 Common workflows

- Local quick test:

```bash
# terminal 1 - start proxy
python proxy.py

# terminal 2 - serve frontend
python -m http.server 8000
# then open http://localhost:8000
```

- Debugging the transaction list:
	1. Ensure `proxy.py` is running and shows `Server running on http://localhost:<PORT>`
	2. From your machine, call the API directly to check it returns JSON:

```bash
curl "http://localhost:9090/api/txlist?address=0x295a6a847e3715f224826aa88156f356ac523eef"
```

If that returns valid JSON, reload the page and confirm the browser console has no CORS or network errors.

---


## 🚀 Deployment options (what will work once deployed)

Note: This repository is already linked to 4EVERLAND for automatic deployments on changes pushed to the connected GitHub branch. Because 4EVERLAND performs deployments directly from the repository, you do not need an extra GitHub Actions workflow to trigger site uploads. To avoid duplicate deployment actions, the repository's simple GH Actions deploy workflow (if present) has been disabled (push trigger removed).

1) Static hosting only (4EVERLAND static):
 	 - Deploy `index.html` + `styles.css` as static files. The UI will load, but live transactions require a server-side proxy.

2) Static hosting + serverless proxy (recommended):
 	 - Deploy the static files to 4EVERLAND and run the proxy as a serverless function (or use the Cloudflare Worker provided in the repo). This keeps API keys secret and preserves live features.

3) Cloudflare Worker (preferred for secrets):
 	 - Use the Worker (see `worker/index.js`) to proxy Etherscan calls. Workers provide secure secret storage and low-latency edge requests.

4) Exposing keys client-side (NOT recommended):
 	 - You can call Etherscan directly from the browser, but this exposes your API key and will quickly hit rate limits.

---

## 🔧 Troubleshooting & tips

- "Failed to fetch" in the browser:
	- Ensure the proxy is running and reachable at the expected port.
	- Confirm the page's JS is configured to use the correct proxy port (the code auto-detects `localhost`).
	- Check browser console for CORS/network errors. The proxy returns `Access-Control-Allow-Origin: *`.

- Wrong port / duplicate script issues:
	- If you edited `index.html` earlier, ensure there are no duplicate `<script>` blocks that reference a different port.

- Port already in use:
	- Change `PORT` in `.env` and restart `proxy.py`.

- Etherscan rate limits / API errors:
	- Use a valid Etherscan V2 key. For heavy usage consider caching or an alternative provider.

---

## 📂 Project files

```
.env                  # Environment variables (create from template above)
index.html            # Frontend UI (contains the transaction & mint UI)
styles.css            # Page styling
proxy.py              # Python proxy server that calls Etherscan & provider
worker/               # Cloudflare Worker (optional) for serverless proxy
```

---

## 📌 Quick verification commands

```bash
# Start proxy (reads .env)
python proxy.py

# Serve static UI
python -m http.server 8000

# Test API directly
curl "http://localhost:9090/api/txlist?address=0x295a6a847e3715f224826aa88156f356ac523eef"
```

---

If you'd like, I can add a small `run.sh`/`run.ps1` script to start both the proxy and the static server together, or scaffold a simple GitHub Action that deploys the static site and the worker to 4EVERLAND/Cloudflare.

---

© iZND Group
