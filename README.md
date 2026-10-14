# python-utils-45

A lightweight, high-performance toolkit for crypto developers designed to streamline blockchain data ingestion and wallet management. This library simplifies complex cryptographic operations and provides robust utilities for interacting with multi-chain environments.

## Features

*   **Address Validation Engine:** Built-in regex and checksum verification for BTC, ETH, and SOL wallet formats.
*   **Asynchronous Price Aggregator:** Efficient multi-source fetcher for real-time asset pricing with built-in rate-limiting and cache support.
*   **Transaction Signing Helpers:** Simplified interface for constructing and broadcasting raw transactions without manual hex-encoding.
*   **Key Security Utilities:** Secure mnemonic generation and derivation path management compliant with BIP-39 and BIP-44 standards.

## Installation

Install the package directly from PyPI:

```bash
pip install python-utils-45
```

Alternatively, for the latest development build:

```bash
git clone https://github.com/Developer/python-utils-45.git
cd python-utils-45
pip install -r requirements.txt
```

## Usage

Quickly validate an Ethereum address and fetch its current balance through the integrated module:

```python
from pyutils45 import WalletManager, PriceEngine

# Validate an address
validator = WalletManager(network='ethereum')
if validator.is_valid("0x71C7656..."):
    print("Address verified.")

# Fetch real-time market data
engine = PriceEngine()
price = engine.get_latest_price("BTC", "USD")
print(f"Current BTC Price: ${price}")
```

## Contributing

We welcome contributions from the crypto-engineering community. Please ensure all pull requests pass the existing test suite and adhere to PEP 8 standards.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.