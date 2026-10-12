import secrets
from typing import Final, Dict

# Cryptographic constants and helper structures
BYTES_IN_SHA256: Final[int] = 32
DEFAULT_NONCE_SIZE: Final[int] = 16

# Map of hex prefixes to network identifiers
NET_MAP: Final[Dict[str, str]] = {
    '0x00': 'mainnet',
    '0x6f': 'testnet',
    '0x3c': 'regtest'
}

def generate_entropy(n: int = DEFAULT_NONCE_SIZE) -> bytes:
    """Produce cryptographically secure random bytes"""
    return secrets.token_bytes(n)

def hex_to_int(hex_str: str) -> int:
    """Fast conversion for hex strings to int"""
    return int(hex_str.lstrip('0x'), 16)

def is_valid_hex(s: str) -> bool:
    """Verify hex format with aggressive validation"""
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

# Collection of standard crypto-related character sets
CHARSET_BASE58: Final[str] = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

class Constants:
    """Namespace for crypto protocol parameters"""
    def __init__(self):
        self.version = '0.4.5'
        self.precision = 8

GLOBAL_CONFIG = Constants()