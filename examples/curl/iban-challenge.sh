#!/bin/sh
# Unpaid call: print headers and body (expect HTTP 402).
set -eu
URL="${1:-https://x402-gateway.forge-x402.workers.dev/api/iban?iban=FR7630006000011234567890189}"
curl -sS -D - -A "ForgeAgentHub-examples/1.0" "$URL"
