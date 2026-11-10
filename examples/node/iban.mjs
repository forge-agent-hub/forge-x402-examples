/**
 * Call the IBAN endpoint.
 * Without EVM_PRIVATE_KEY: print the HTTP 402 challenge and exit 0.
 * With EVM_PRIVATE_KEY: pay with @x402/fetch (x402 v2) and print the JSON result.
 */
const URL =
  process.env.API_URL ||
  "https://x402-gateway.forge-x402.workers.dev/api/iban?iban=FR7630006000011234567890189";

async function unpaid() {
  const res = await fetch(URL, { headers: { accept: "application/json", "user-agent": "ForgeAgentHub-examples/1.0" } });
  const text = await res.text();
  console.log("status", res.status);
  console.log(text);
  if (res.status !== 402) {
    console.error("Expected HTTP 402 on an unpaid call.");
    process.exit(1);
  }
}

async function paid(pk) {
  const { wrapFetchWithPaymentFromConfig } = await import("@x402/fetch");
  const { ExactEvmScheme } = await import("@x402/evm");
  const { privateKeyToAccount } = await import("viem/accounts");
  const account = privateKeyToAccount(pk);
  const fetchWithPayment = wrapFetchWithPaymentFromConfig(fetch, {
    schemes: [{ network: "eip155:8453", client: new ExactEvmScheme(account) }],
  });
  const res = await fetchWithPayment(URL);
  console.log("status", res.status);
  console.log(await res.text());
}

const pk = process.env.EVM_PRIVATE_KEY;
if (!pk) {
  await unpaid();
} else {
  if (!/^0x[0-9a-fA-F]{64}$/.test(pk)) {
    console.error("EVM_PRIVATE_KEY must be a 0x-prefixed 32-byte hex key.");
    process.exit(2);
  }
  await paid(pk);
}
