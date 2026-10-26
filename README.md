# python-utils-45

A lightweight Python toolkit designed for high-performance cryptocurrency data analysis and automated market monitoring. It provides efficient abstractions for interfacing with major exchange APIs and executing technical analysis on live order book data.

## Features

*   **Asynchronous Exchange Client:** Built on `ccxt` with custom retry logic and connection pooling to ensure zero downtime during high-volatility events.
*   **Real-time TA Engine:** Implements high-speed vectorized indicators (RSI, MACD, Bollinger Bands) optimized for large-scale candle data processing.
*   **WebSocket Stream Manager:** Handles multi-pair socket subscriptions with automated heartbeat monitoring and automatic reconnection handling.
*   **Data Normalization Layer:** Standardizes disparate API response formats from various exchanges into a unified schema for consistent analysis.

## Installation

Ensure you have Python 3.9+ installed. Install the package via pip:

```bash
pip install python-utils-45
```

For development mode, clone the repository and run:

```bash
git clone https://github.com/Developer/python-utils-45.git
cd python-utils-45
pip install -r requirements.txt
```

## Usage

A quick example to fetch live price data and calculate the current RSI for BTC/USDT:

```python
from utils_45.client import CryptoClient
from utils_45.analysis import TechnicalEngine

client = CryptoClient(exchange="binance")
engine = TechnicalEngine()

# Fetch latest 100 1h candles
data = client.get_ohlcv("BTC/USDT", timeframe="1h", limit=100)

# Compute RSI
rsi = engine.calculate_rsi(data, period=14)
print(f"Current RSI: {rsi[-1]}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.