from typing import Final, Dict

# Crypto asset protocol mappings and operational thresholds
BLOCK_TIME_SECONDS: Final[float] = 12.5
MAX_RETRY_ATTEMPTS: Final[int] = 5

# Network identifiers for blockchain integration
NETWORK_MAP: Final[Dict[str, str]] = {
    "ETH": "ethereum",
    "BTC": "bitcoin",
    "SOL": "solana"
}

# Cryptographic security constants
DERIVATION_PATH: Final[str] = "m/44'/60'/0'/0/0"
MIN_FEE_THRESHOLD: Final[float] = 0.000005

class CryptoConfig:
    __slots__ = ('network_id', 'precision')
    
    def __init__(self, network: str, precision: int = 8):
        self.network_id = NETWORK_MAP.get(network, "unknown")
        self.precision = precision

# Default session configuration instance
DEFAULT_SESSION = CryptoConfig("ETH")

# Standardized status codes for crypto processing pipeline
SUCCESS_CODE: Final[str] = "0x00"
FAILURE_CODE: Final[str] = "0x01"
PENDING_CODE: Final[str] = "0x02"