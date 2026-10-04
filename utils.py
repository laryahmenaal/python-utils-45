import hashlib
import hmac
import base64
from typing import Any, Dict

def derive_nonce(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()[:16]

def sign_payload(secret: str, message: str) -> str:
    return hmac.new(secret.encode(), message.encode(), hashlib.sha512).hexdigest()

def obfuscate_key(key: str) -> str:
    return base64.b64encode(key[::-1].encode()).decode()

def normalize_amount(value: Any) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def validate_transaction_integrity(data: Dict[str, Any], signature: str, secret: str) -> bool:
    payload = "|".join([str(v) for v in data.values()])
    return hmac.compare_digest(sign_payload(secret, payload), signature)

class CryptoBuffer:
    def __init__(self, capacity: int = 1024):
        self._storage = bytearray(capacity)
        self._ptr = 0

    def write(self, data: bytes):
        length = len(data)
        if self._ptr + length > len(self._storage):
            self._storage.extend(bytearray(length * 2))
        self._storage[self._ptr:self._ptr + length] = data
        self._ptr += length

    def get_data(self) -> bytes:
        return bytes(self._storage[:self._ptr])