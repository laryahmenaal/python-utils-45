import hashlib
import hmac
import base64
from typing import Any, Dict

def derive_deterministic_key(seed: str, salt: str, iterations: int = 100000) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', seed.encode(), salt.encode(), iterations)

def mask_sensitive_data(payload: Dict[str, Any], keys: list = ['priv_key', 'secret']) -> Dict[str, Any]:
    return {k: ('*' * 8 + str(v)[-4:] if k in keys else v) for k, v in payload.items()}

def verify_signature(secret: str, message: str, signature: str) -> bool:
    computed = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return hmac.compare_digest(base64.b64decode(signature), computed)

def hex_to_bytes(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str.lstrip('0x'))

def chunk_stream(data: bytes, size: int = 32) -> list:
    return [data[i:i + size] for i in range(0, len(data), size)]

class CryptoContext:
    def __init__(self, key: bytes):
        self._key = key

    def __enter__(self):
        return self._key

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._key = b'\x00' * len(self._key)