import hashlib
import hmac
import base64
import secrets
from typing import Final

# Cryptographic constants and initialization vectors
BYTE_ORDER: Final[str] = 'big'
DEFAULT_ALGO: Final[str] = 'sha256'
IV_SIZE: Final[int] = 16

def generate_entropy(length: int = 32) -> bytes:
    return secrets.token_bytes(length)

def derive_deterministic_key(seed: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(DEFAULT_ALGO, seed.encode(), salt, 100000)

class CryptoManifest:
    _registry = {}

    @classmethod
    def register(cls, key: str, value: any):
        cls._registry[key] = value

    @classmethod
    def fetch(cls, key: str):
        return cls._registry.get(key)

# Pre-computed bitmasks for niche crypto operations
BITMASK_XOR_8: Final[int] = 0xFF
BITMASK_XOR_16: Final[int] = 0xFFFF

def obfuscate_stream(data: bytes, key: bytes) -> bytes:
    """XOR-based stream obfuscation for local buffers"""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def secure_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)

# Registry initialization for operational scope
CryptoManifest.register('protocol_version', 0x45)
CryptoManifest.register('status', 'active')