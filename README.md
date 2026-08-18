# python-utils-45

A collection of utility functions for cryptocurrency data analysis and trading automation in Python. This project aims to simplify common tasks for developers working with various crypto APIs and facilitate quick prototyping of trading strategies.

## Features

- **API Integration**: Seamlessly interact with major cryptocurrency exchanges like Binance and Coinbase, with built-in methods to fetch market data, order book information, and account balances.
- **Data Visualization**: Generate insightful visualizations of price trends, trading volumes, and historical performance using matplotlib and seaborn.
- **Time-Series Analysis**: Built-in support for common time-series analysis functions, including moving averages, RSI, and MACD, to assist in strategy development.
- **Trade Simulation**: Simulate trades and backtest strategies using historical data to evaluate performance before going live.

## Installation

To get started with `python-utils-45`, clone the repository and install the required dependencies:

```bash
git clone https://github.com/your_username/python-utils-45.git
cd python-utils-45
pip install -r requirements.txt
```

## Basic Usage

Here’s a quick example of how to use the library to fetch current price data and plot it:

```python
from utils.crypto_api import CryptoAPI
from utils.visualization import plot_price_trend

# Initialize the API client
api = CryptoAPI(exchange='binance', api_key='YOUR_API_KEY')

# Fetch current price for Bitcoin
btc_price = api.get_current_price('BTC/USDT')
print(f"Current BTC Price: {btc_price}")

# Fetch historical data for plotting
historical_data = api.get_historical_data('BTC/USDT', period='7d')

# Plot price trend
plot_price_trend(historical_data)
```

For more detailed documentation and examples, please visit the [Wiki](https://github.com/your_username/python-utils-45/wiki).

## License

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.