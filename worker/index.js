export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // route API endpoints
    if (path.startsWith('/api/txlist')) {
      return handleTxlist(url.searchParams, env);
    }
    if (path.startsWith('/api/mints')) {
      return handleMints(url.searchParams, env);
    }
    if (path.startsWith('/api/logs')) {
      return handleLogs(url.searchParams, env);
    }

    return new Response('Not Found', { status: 404 });
  }
};

async function handleTxlist(params, env) {
  const address = params.get('address');
  if (!address) return jsonResponse({ error: 'address query parameter required' }, 400);
  const apiKey = env.ETHERSCAN_API_KEY || '';
  const url = `https://api.etherscan.io/v2/api?chainid=1&module=account&action=txlist&address=${address}&sort=desc&apikey=${apiKey}`;
  try {
    const resp = await fetch(url, { method: 'GET' });
    const text = await resp.text();
    return new Response(text, { status: resp.status, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } });
  } catch (e) {
    return jsonResponse({ error: 'proxy_exception', message: String(e) }, 500);
  }
}

async function handleMints(params, env) {
  const address = params.get('address');
  const page = params.get('page') || '1';
  const offset = params.get('offset') || '100';
  if (!address) return jsonResponse({ error: 'address query parameter required' }, 400);
  const apiKey = env.ETHERSCAN_API_KEY || '';
  const url = `https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokennfttx&address=${address}&page=${page}&offset=${offset}&sort=desc&apikey=${apiKey}`;
  try {
    const resp = await fetch(url, { method: 'GET' });
    const text = await resp.text();
    return new Response(text, { status: resp.status, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } });
  } catch (e) {
    return jsonResponse({ error: 'proxy_exception', message: String(e) }, 500);
  }
}

async function handleLogs(params, env) {
  const address = params.get('address');
  const fromBlock = params.get('fromBlock') || '0';
  const toBlock = params.get('toBlock') || 'latest';
  if (!address) return jsonResponse({ error: 'address query parameter required' }, 400);
  const provider = env.PROVIDER_URL;
  if (!provider) return jsonResponse({ error: 'PROVIDER_URL not configured' }, 400);

  const topic0 = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef';
  const paramsObj = [{
    fromBlock: fromBlock === 'latest' ? '0x0' : '0x' + parseInt(fromBlock).toString(16),
    toBlock: toBlock === 'latest' ? 'latest' : '0x' + parseInt(toBlock).toString(16),
    address: address,
    topics: [topic0]
  }];

  try {
    const rpc = { jsonrpc: '2.0', id: 1, method: 'eth_getLogs', params: paramsObj };
    const resp = await fetch(provider, { method: 'POST', body: JSON.stringify(rpc), headers: { 'Content-Type': 'application/json' } });
    const data = await resp.json();
    const logs = data.result || [];
    const parsed = logs.map(log => {
      const topics = log.topics || [];
      let tokenId = null, from = null, to = null;
      if (topics.length >= 4) {
        from = '0x' + topics[1].slice(-40);
        to = '0x' + topics[2].slice(-40);
        tokenId = parseInt(topics[3], 16);
      } else {
        try { tokenId = parseInt(log.data, 16); } catch(e) { tokenId = null; }
      }
      return { blockNumber: parseInt(log.blockNumber || '0', 16), transactionHash: log.transactionHash, from, to, tokenId, logIndex: parseInt(log.logIndex || '0', 16) };
    });
    return jsonResponse({ status: '1', message: 'OK', result: parsed });
  } catch (e) {
    return jsonResponse({ error: 'provider_error', message: String(e) }, 502);
  }
}

function jsonResponse(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } });
}
