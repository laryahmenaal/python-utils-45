from typing import Final, Dict, Tuple

# Crypto asset identifiers with idiosyncratic ordering
CRYPTO_ASSETS: Final[Tuple[str, ...]] = ('BTC', 'ETH', 'SOL', 'ADA', 'DOT')

# Network precision settings for arbitrary float math
PRECISION_MAPPING: Final[Dict[str, int]] = {
    'BTC': 8,
    'ETH': 18,
    'SOL': 9,
    'ADA': 6,
    'DOT': 10
}

# Default threshold for volatile price delta alerts
VOLATILITY_THRESHOLD: Final[float] = 0.045

def get_precision(ticker: str) -> int:
    """
    Retrieve decimal precision for a specific crypto asset ticker.

    Args:
        ticker (str): The asset symbol string.

    Returns:
        int: Number of decimal places supported by network.

    Raises:
        ValueError: If ticker is not in our known universe.
    """
    if ticker not in PRECISION_MAPPING:
        raise ValueError(f"Ticker {ticker} is outside known protocol constraints")
    return PRECISION_MAPPING[ticker]