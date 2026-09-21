# python-utils-45

`python-utils-45` is a high-performance Python toolkit designed to streamline common tasks in cryptocurrency trading and blockchain data analysis. It provides robust wrappers for exchange APIs and specialized math utilities for calculating portfolio metrics and market volatility.

## Features

*   **Exchange Abstraction Layer:** Standardized interface to interact with major CEXs (Binance, Kraken, Coinbase) using unified request logic and rate-limit handling.
*   **Real-time Orderbook Analytics:** Optimized functions for calculating Mid-price, Spread, and Orderbook Imbalance with low-latency execution.
*   **Backtesting Utilities:** Lightweight simulation engine to compute Sharpe ratios, Maximum Drawdown, and ROI on historical OHLCV data.
*   **Security Signing Helpers:** Built-in HMAC-SHA256 signature generation to securely authenticate private API requests without boilerplate overhead.

## Installation

Install the package via pip:

```bash
pip install python-utils-45
```

For development mode and access to experimental indicators:

```bash
git clone https://github.com/Developer/python-utils-45.git
cd python-utils-45
pip install -r requirements.txt
```

## Usage Example

Easily fetch ticker data and compute volatility using the library's streamlined core:

```python
from crypto_utils import ExchangeClient, Analytics

# Initialize exchange client
client = ExchangeClient(api_key='YOUR_KEY', secret='YOUR_SECRET')

# Fetch live ticker for BTC/USDT
ticker = client.get_ticker('BTC/USDT')

# Calculate 24h rolling volatility
vol = Analytics.calculate_volatility(ticker.history(days=1))

print(f"BTC Current Price: {ticker.price}")
print(f"Rolling Volatility: {vol:.4f}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.