# AI-Powered Web3 Solutions by iZND Group

Welcome to the **AI-Powered Web3 Solutions** project! This site showcases how iZND Group leverages Microsoft AI and blockchain technology to deliver next-generation automation, security, and NFT innovation.

---

## 🚀 Features

- **AI-Powered Web3 Services**: Explore a range of AI-driven blockchain solutions, including smart contract automation, NFT creation, and enterprise tokenization.
- **TheAlien.888 Success Story**: Learn how AI autonomously generated, structured, and deployed the TheAlien.888 NFT collection.
- **Live Blockchain Verification**: View real-time Ethereum transactions and contract verification via Etherscan.
- **NFT Marketplace**: Browse and trade AI-generated NFTs in the integrated marketplace.
- **Mint Your Own NFT**: Mint a unique TheAlien.888 NFT directly from the site in a mobile-friendly popup.
- **Modern, Responsive UI**: Clean navigation, responsive design, and easy access to all sections.

---

## 🛠️ Tech Stack

- **HTML5 & CSS3**: Modern, responsive layout and styling.
- **JavaScript**: Dynamic transaction and mint tracker using the Etherscan API.
- **Etherscan API**: Live blockchain data and NFT mint tracking.
- **Microsoft AI**: Integration and inspiration for AI-driven blockchain solutions.

---

## 📄 How to Use

1. **Clone or Download** this repository.
2. Create a `.env` file (or set environment variables) using `.env.example` as a template and fill in your keys:

```
ETHERSCAN_API_KEY=your_etherscan_api_key_here
PROVIDER_URL=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
PORT=8080
```

3. Start the local proxy which serves the site and proxies Etherscan/JSON-RPC calls:

```powershell
python proxy.py
```

4. Open the site in your browser (served over HTTP):

```
http://localhost:8080/index.html
```

5. The frontend will call these local endpoints:
- `/api/txlist?address=...` — Etherscan V2 `txlist` (live transactions)
- `/api/mints?address=...` — Etherscan V2 `tokennfttx` (ERC-721 transfer history)
- `/api/logs?address=...&fromBlock=0&toBlock=latest` — JSON-RPC `eth_getLogs` (fallback used to reliably detect Transfer events and mints)

6. Example curl tests:

```bash
curl -s "http://localhost:8080/api/txlist?address=0x295a6a847e3715f224826aa88156f356ac523eef" | jq .
curl -s "http://localhost:8080/api/mints?address=0x295a6a847e3715f224826aa88156f356ac523eef&page=1&offset=100" | jq .
curl -s "http://localhost:8080/api/logs?address=0x295a6a847e3715f224826aa88156f356ac523eef&fromBlock=0&toBlock=latest" | jq .
```

Notes:
- `PROVIDER_URL` is required for the `/api/logs` fallback. Use an Infura/Alchemy/QuickNode HTTP RPC URL.
- Do not open the site via `file://` — the proxy serves assets and enables CORS for API calls.

---

**Automatic Deployment to 4EVERLAND (CI)**

This repository includes a GitHub Actions workflow template at `.github/workflows/deploy-4everland.yml` that archives `index.html`, `styles.css`, and other HTML files and uploads them to 4EVERLAND.

How it works (high level):
- On push to `main`, the workflow archives the site into `site.zip`.
- The workflow uses two repository secrets that you must set (see below) and then uploads the archive to 4EVERLAND using their upload API/CLI. The workflow contains placeholders where 4EVERLAND's exact upload endpoint/params should be inserted according to 4EVERLAND docs.

Required repository secrets (create these in GitHub Settings → Secrets):
- `FOREVERLAND_API_KEY` — an API key / token from your 4EVERLAND dashboard.
- `FOREVERLAND_API_URL` — the upload API base URL (example placeholder used in the workflow). Use the URL or CLI command specified by 4EVERLAND docs.
- Optional: `FOREVERLAND_DEPLOY_URL` — the published URL (gateway) returned by 4EVERLAND after upload; the workflow can run a simple health-check against it.

How to customize:
- Replace the `curl` upload command in `.github/workflows/deploy-4everland.yml` with the exact upload/CLI invocation from 4EVERLAND docs.
- If 4EVERLAND provides a CLI, you can install it in the workflow and call it instead of `curl`.

If you prefer, I can update the workflow with the exact 4EVERLAND CLI or API call once you provide the upload endpoint or confirm which 4EVERLAND product (Static Hosting / Buckets / DWeb Hosting) you want to use.
 
---

**Cloudflare Worker proxy (recommended)**

This repo now includes a Cloudflare Worker in the `worker/` folder which implements the same proxy endpoints as `proxy.py` (`/api/txlist`, `/api/mints`, `/api/logs`) so you can keep secrets server-side and avoid exposing API keys in the browser.

Deployment notes:
- Add `CF_API_TOKEN` repository secret (a Cloudflare API token with Worker write permissions).
- Add `CF_ACCOUNT_ID` if required by your Wrangler configuration.
- Add `ETHERSCAN_API_KEY` and `PROVIDER_URL` as Cloudflare Worker secrets (via `wrangler secret put` or the Cloudflare dashboard) so the Worker can call Etherscan and your JSON-RPC provider.

Set the `PROXY_URL` secret in GitHub to your Cloudflare Worker URL (for example: `https://your-worker.example.workers.dev`). The workflow will replace the `__PROXY_URL__` placeholder in `index.html` before uploading the static site so the frontend calls the correct proxy endpoint.

The GitHub Action will attempt to publish the Worker automatically after uploading static files to 4EVERLAND. You must configure the Cloudflare secrets and the 4EVERLAND secrets in the repository settings for the workflow to complete automatically.

---

## 🔗 Useful Links

- [iZND Group Main Site](https://www.izndgroup.com)
- [Microsoft AI](https://www.microsoft.com/en-us/ai)
- [TheAlien.888 Marketplace](https://marketplace.thealien888.iznd.xyz)
- [Smart Contract on Etherscan](https://etherscan.io/address/0x295a6a847e3715f224826aa88156f356ac523eef)

---

## 📦 Project Structure

```
index.html         # Main website file
styles.css         # Custom styles
README.md          # This file
```

---

## 📝 License

This project is for demonstration and educational purposes.  
For commercial use or partnership, please contact [iZND Group](https://www.izndgroup.com/contact-us).

---

## 🤖 Credits

- Built by iZND Group, powered by Microsoft AI and blockchain technology.