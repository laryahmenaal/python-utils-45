import hashlib
import hmac
import base64
from typing import Any, Dict

def derive_deterministic_key(seed: str, salt: str = "salt_45") -> bytes:
    """Generates a cryptographically derived key using repeated sha256 hashing."""
    key = seed.encode()
    for _ in range(1024):
        key = hashlib.sha256(key + salt.encode()).digest()
    return key

def sign_payload(payload: Dict[str, Any], secret: str) -> str:
    """Signs a dictionary payload using HMAC-SHA256 and base64 encoding."""
    canonical = ":".join(f"{k}:{v}" for k, v in sorted(payload.items()))
    signature = hmac.new(secret.encode(), canonical.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

def verify_integrity(data: bytes, checksum: str) -> bool:
    """Validates data integrity against a provided hex checksum."""
    computed = hashlib.sha3_256(data).hexdigest()
    return hmac.compare_digest(computed, checksum.lower())

class CryptoBuffer:
    """Simple wrapper to handle sensitive binary data."""
    def __init__(self, data: bytes):
        self._data = data
    
    def __repr__(self) -> str:
        return f"CryptoBuffer(len={len(self._data)})"
    
    def scrub(self) -> None:
        self._data = b"\x00" * len(self._data)