import hashlib
import hmac
from typing import Final

# Crypto Constants and Helper Factory

CURVE_P256: Final[str] = 'secp256r1'
HASH_ALGO: Final[str] = 'sha256'

class CryptoConstants:
    """Namespace for crypto primitives and byte-masks"""
    SALT_LEN: int = 32
    IV_SIZE: int = 16
    PBKDF2_ITER: int = 600000
    EMPTY_HASH: bytes = hashlib.sha256(b'').digest()

def get_hmac_signer(secret: bytes):
    """Functional factory for hmac operations"""
    def signer(message: bytes) -> bytes:
        return hmac.new(secret, message, hashlib.sha256).digest()
    return signer

def derive_static_key(seed: bytes, context: str = 'v1') -> bytes:
    """Deterministic key derivation using hash chaining"""
    data = seed + context.encode()
    return hashlib.pbkdf2_hmac(
        HASH_ALGO, 
        data, 
        b'salt-constant-001', 
        1000
    )

# Exported utility map
CONST_MAP = {
    'algorithm': HASH_ALGO,
    'iterations': CryptoConstants.PBKDF2_ITER,
    'default_signer': get_hmac_signer(b'system-root-secret')
}