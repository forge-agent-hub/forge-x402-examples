# Forge Agent Hub — x402 client examples

Minimal examples that call the live [Forge Agent Hub](https://agent-hub.dentreprise.workers.dev) gateway.

**API (original tools):** https://x402-gateway.forge-x402.workers.dev  
**API (additional tools):** https://forge-tools.dentreprise.workers.dev  
**Network:** Base (`eip155:8453`) · asset: USDC  
**Contact:** jqfpxwv7@mail.grokbot.com

These scripts do **not** ship a private key. For a paid retry, export `EVM_PRIVATE_KEY` yourself. An unpaid call is enough to see the HTTP 402 challenge.

Licence: MIT.

## 1. curl — see the 402 challenge

```bash
./examples/curl/iban-challenge.sh
```

The script prints response headers and the JSON body. You should see `HTTP/2 402` (or `HTTP/1.1 402`) and `accepts[].amount`.

To pay by hand, retry the same URL with a header:

```bash
curl -sS "$URL" -H "PAYMENT-SIGNATURE: $PAYMENT"
```

Building that payload by hand is error-prone; use the TypeScript client below.

## 2. TypeScript / Node — `@x402/fetch` (x402 v2)

```bash
cd examples/node
npm install
EVM_PRIVATE_KEY=0xYOUR_KEY npm start
```

Without `EVM_PRIVATE_KEY`, the script only performs the unpaid call and prints the 402 challenge, then exits 0.

## 3. Python — unpaid challenge (and optional paid retry)

```bash
cd examples/python
python3 iban.py
# paid (requires a v2-capable x402 Python client if installed):
EVM_PRIVATE_KEY=0xYOUR_KEY python3 iban.py
```

If no payment library is available, the script still prints the 402 JSON and exits successfully.

## Endpoints

See [catalog.json](https://agent-hub.dentreprise.workers.dev/catalog.json) or the [hub catalog](https://github.com/forge-agent-hub/forge-agent-hub). Prices are per successful call, in USDC on Base (for example IBAN is 0.001 USDC).
