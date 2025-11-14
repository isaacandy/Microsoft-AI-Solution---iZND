const path = require('path');
const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY;

if (!ETHERSCAN_API_KEY) {
    console.warn('Warning: ETHERSCAN_API_KEY is not set. Set it in a .env file or environment before starting the server.');
}

app.use(express.json());
app.use(cors());

// --- API routes registered BEFORE static file serving to avoid static 404s ---
app.get('/api/txlist', async (req, res) => {
    try {
        const { address } = req.query;
        if (!address) return res.status(400).json({ error: 'address query parameter required' });

        const url = `https://api.etherscan.io/api/v2/accounts/${address}/transactions?sort=desc`;
        const response = await axios.get(url, {
            headers: {
                'X-API-KEY': ETHERSCAN_API_KEY || ''
            },
            timeout: 15000
        });
        return res.status(200).json(response.data);
    } catch (err) {
        console.error('Error proxying txlist:', err && err.toString());
        const status = err.response ? err.response.status : 500;
        const data = err.response ? err.response.data : { error: err.message };
        return res.status(status).json(data);
    }
});

app.get('/api/mints', async (req, res) => {
    try {
        const { address, page = 1, offset = 100 } = req.query;
        if (!address) return res.status(400).json({ error: 'address query parameter required' });

        const url = `https://api.etherscan.io/api/v2/accounts/${address}/transactions/erc721?sort=desc&page=${page}&offset=${offset}`;
        const response = await axios.get(url, {
            headers: {
                'X-API-KEY': ETHERSCAN_API_KEY || ''
            },
            timeout: 15000
        });
        return res.status(200).json(response.data);
    } catch (err) {
        console.error('Error proxying mints:', err && err.toString());
        const status = err.response ? err.response.status : 500;
        const data = err.response ? err.response.data : { error: err.message };
        return res.status(status).json(data);
    }
});

// Serve static site from the repository root (after API routes)
app.use(express.static(path.join(__dirname)));

// Fallback: serve index.html for unknown non-API routes (simple SPA support)
app.get('*', (req, res) => {
    if (req.path.startsWith('/api/')) return res.status(404).json({ error: 'API endpoint not found' });
    return res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
