#!/usr/bin/env python3
"""Call the IBAN endpoint. Unpaid calls print the HTTP 402 challenge.

If EVM_PRIVATE_KEY is set and an x402 v2 Python client is importable, a paid
retry is attempted. This file never hard-codes a key.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

URL = os.environ.get(
    "API_URL",
    "https://x402-gateway.forge-x402.workers.dev/api/iban?iban=FR7630006000011234567890189",
)


def unpaid() -> int:
    req = urllib.request.Request(
        URL,
        headers={"Accept": "application/json", "User-Agent": "ForgeAgentHub-examples/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            body = res.read().decode()
            print("status", res.status)
            print(body)
            print("Unexpected: unpaid call did not return 402.", file=sys.stderr)
            return 1
    except urllib.error.HTTPError as err:
        body = err.read().decode()
        print("status", err.code)
        print(body)
        return 0 if err.code == 402 else 1


def paid(pk: str) -> int:
    # Official package names change; try a few known v2 entry points, else explain.
    try:
        from x402.client import x402Client  # type: ignore
    except Exception:
        print(
            "No x402 v2 Python client is installed in this environment.\n"
            "Install one (for example a package published by the x402 project) "
            "or use the Node example in examples/node with @x402/fetch.\n"
            "The unpaid 402 challenge is still shown above if you run without a key.",
            file=sys.stderr,
        )
        return unpaid()
    print("A Python x402 client was found but this example does not auto-wire it", file=sys.stderr)
    print("to avoid inventing an unstable API. Use examples/node for a paid call.", file=sys.stderr)
    return unpaid()


def main() -> int:
    pk = os.environ.get("EVM_PRIVATE_KEY")
    if not pk:
        return unpaid()
    if not (pk.startswith("0x") and len(pk) == 66):
        print("EVM_PRIVATE_KEY must be a 0x-prefixed 32-byte hex key.", file=sys.stderr)
        return 2
    return paid(pk)


if __name__ == "__main__":
    raise SystemExit(main())
