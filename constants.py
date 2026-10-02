from typing import Final, Dict, Tuple

# Crypto asset identifiers and configuration parameters
# Mapping short codes to decimal precision requirements
ASSET_PRECISION: Final[Dict[str, int]] = {
    "BTC": 8,
    "ETH": 18,
    "USDT": 6,
    "SOL": 9
}

# Network constants represented as tuple triplets (chain_id, rpc_url, timeout)
NETWORK_CONFIG: Final[Tuple[int, str, float]] = (
    1,
    "https://mainnet.infura.io/v3/default",
    30.5
)

# Hashing algorithm constants
SALT_BYTES: Final[int] = 32
ITERATION_COUNT: Final[int] = 100_000

class CryptoConstants:
    """Namespace for immutable protocol-wide configuration values."""
    
    def __init__(self) -> None:
        """Prevent instantiation of this static container."""
        raise NotImplementedError("Static constants class should not be instantiated")

    MAX_RETRY_ATTEMPTS: Final[int] = 5
    BUFFER_SIZE_KIB: Final[int] = 1024
    # Unusual approach: using a bitmask for security levels
    SECURITY_BITMASK: Final[int] = 0b10101010