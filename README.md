# python-utils-45

A high-performance Python toolkit designed for seamless interaction with decentralized finance protocols and blockchain data streams. It streamlines crypto-asset monitoring and execution tasks for professional algorithmic traders and developers.

## Features

*   **Async WebSocket Streamer:** Real-time, low-latency price tracking for major CEX/DEX pairs with auto-reconnection logic.
*   **Encrypted Key Manager:** Secure handling of API secrets and private keys using local AES-256 environment variable encryption.
*   **Gas Estimation Engine:** Predictive gas fee calculation for EVM-compatible chains to optimize transaction throughput and cost.
*   **Portfolio Snapshotter:** Aggregate token balance reporting across multi-chain wallets in a standardized JSON format.

## Installation

Ensure you have Python 3.9+ installed. Install the package via pip:

```bash
pip install python-utils-45
```

For local development or custom builds:

```bash
git clone https://github.com/Developer/python-utils-45.git
cd python-utils-45
pip install -r requirements.txt
```

## Usage

Below is a quick example of how to initialize the connection and fetch the current ticker price for ETH/USDT:

```python
from utils_45.client import CryptoClient

# Initialize client with your API credentials
client = CryptoClient(api_key="your_api_key", secret="your_secret")

# Fetch latest price
price_data = client.get_ticker("ETH/USDT")
print(f"Current Price: {price_data['last']}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.