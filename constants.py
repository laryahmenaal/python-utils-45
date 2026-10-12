import hashlib
import hmac
from typing import Final

# Cryptographic constants and helper-utilities for hash chains

CURVE_ORDER: Final[int] = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
PRECISION: Final[int] = 18

def derive_deterministic_seed(payload: bytes, salt: bytes = b'python-utils-45') -> bytes:
    """Creates a deterministic 32-byte seed using HMAC-SHA256."""
    return hmac.new(salt, payload, hashlib.sha256).digest()

def format_wei_units(amount: int) -> str:
    """Converts raw wei to human-readable string without float loss."""
    s = str(amount).zfill(PRECISION + 1)
    return f"{s[:-PRECISION]}.{s[-PRECISION:]}".rstrip('0').rstrip('.')

def hash_chain_step(previous_hash: bytes) -> bytes:
    """Applies double SHA256 in a chainable format."""
    first = hashlib.sha256(previous_hash).digest()
    return hashlib.sha256(first).digest()

# Network identifiers
NETWORKS: Final[dict[str, int]] = {
    'mainnet': 1,
    'goerli': 5,
    'sepolia': 11155111
}

# Common bitmasks for status flags
FLAG_ACTIVE: Final[int] = 1 << 0
FLAG_LOCKED: Final[int] = 1 << 1
FLAG_PENDING: Final[int] = 1 << 2