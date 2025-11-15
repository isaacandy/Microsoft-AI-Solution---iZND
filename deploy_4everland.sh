#!/usr/bin/env bash
set -euo pipefail

# Simple deploy script to upload site artifacts to a configurable 4EVERLAND endpoint.
# Usage (locally):
#   export FOURVERLAND_API_URL="https://api.4everland.example/deploy"
#   export FOURVERLAND_API_KEY="<your-key>"
#   ./deploy_4everland.sh

API_URL="${FOUREVERLAND_API_URL:-${FOUREVERLAND_API_URL:-}}"
API_KEY="${FOUREVERLAND_API_KEY:-${FOUREVERLAND_API_KEY:-}}"

if [ -z "$API_URL" ]; then
  echo "ERROR: FOURVERLAND_API_URL is not set. Provide the deploy endpoint URL."
  exit 1
fi

if [ -z "$API_KEY" ]; then
  echo "WARNING: FOURVERLAND_API_KEY is not set. The upload may fail if authentication is required."
fi

TMPZIP="site-deploy-$(date +%s).zip"
echo "Packaging static files into $TMPZIP"
# include typical static assets and worker if present
zip -r "$TMPZIP" index.html styles.css README.md worker || true

echo "Uploading $TMPZIP to $API_URL"
HTTP_STATUS=$(curl -s -o /tmp/deploy_resp.txt -w "%{http_code}" -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -F "file=@${TMPZIP}" \
  "$API_URL")

echo "Response HTTP status: $HTTP_STATUS"
echo "Response body:" && cat /tmp/deploy_resp.txt || true

if [ "$HTTP_STATUS" -ge 200 ] && [ "$HTTP_STATUS" -lt 300 ]; then
  echo "✅ Deploy request succeeded."
  rm -f "$TMPZIP" /tmp/deploy_resp.txt
  exit 0
else
  echo "❌ Deploy request failed. Check the API endpoint and key."
  exit 2
fi
