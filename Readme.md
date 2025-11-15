# Web3 AI Solutions | iZND Group

Live blockchain transactions and NFT mints for **TheAlien.888** on Ethereum.

---

## 🚀 Quick Start

### 1. Set Up Environment

Create a `.env` file in the project root:

```
ETHERSCAN_API_KEY=your_etherscan_v2_api_key
PROVIDER_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
PORT=8080
```

**Get your keys:**
- **Etherscan V2 API Key**: [etherscan.io/apis](https://etherscan.io/apis)
- **Infura/Alchemy JSON-RPC**: [infura.io](https://infura.io) or [alchemy.com](https://alchemy.com)

### 2. Run the Proxy

```bash
python proxy.py
```

Output:
```
✓ Etherscan API Key loaded: YQ1I3BIJV...
✓ Provider URL loaded.

🚀 Server running on http://localhost:8080
📂 Serving files from: C:\Users\...\Microsoft AI Solution - iZND
🌐 Open http://localhost:8080/index.html
⏸  Press Ctrl+C to stop.
```

### 3. Open in Browser

Visit: **http://localhost:8080/index.html**

---

## 🌐 API Endpoints

The proxy exposes three endpoints:

```bash
# Live transactions
GET http://localhost:8080/api/txlist?address=0x295a6a847e3715f224826aa88156f356ac523eef

# NFT mint history (Etherscan)
GET http://localhost:8080/api/mints?address=0x295a6a847e3715f224826aa88156f356ac523eef

# Mint detection via logs (JSON-RPC)
GET http://localhost:8080/api/logs?address=0x295a6a847e3715f224826aa88156f356ac523eef
```

---

## 📂 Project Structure

```
.env                  # Environment variables (create from template below)
index.html            # Frontend UI
styles.css            # Minimal styling
proxy.py              # Python HTTP proxy server
```

---

## 📋 Features

✅ **Live Transactions** — Display Ethereum contract transactions in real-time  
✅ **NFT Mint Tracking** — Show total minted NFTs with highlighting  
✅ **Mint Detection** — Fallback to JSON-RPC logs for reliable mint detection  
✅ **No External Build** — Pure Python + HTML/CSS/JavaScript, zero npm dependencies  
✅ **CORS-Free** — Server-side proxy eliminates browser CORS errors  

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ETHERSCAN_API_KEY not set` | Add `ETHERSCAN_API_KEY=...` to `.env` file |
| `PROVIDER_URL not configured` | Add `PROVIDER_URL=https://...` to `.env` file |
| Port 8080 already in use | Set `PORT=3000` (or any other port) in `.env` |
| `No transactions found` | Contract may have no txs, or API key is invalid |
| No mint data showing | Check `PROVIDER_URL` and ensure it's a valid Infura/Alchemy key |

---

## 🔗 Useful Links

- **Smart Contract**: [etherscan.io/address/0x295a6a84...](https://etherscan.io/address/0x295a6a847e3715f224826aa88156f356ac523eef)
- **iZND Group**: [izndgroup.com](https://www.izndgroup.com)
- **Etherscan API Docs**: [docs.etherscan.io](https://docs.etherscan.io)

---

## 📝 License

For demonstration and educational purposes. Contact iZND Group for commercial use.
