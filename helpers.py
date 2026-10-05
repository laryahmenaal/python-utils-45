import hashlib
import hmac
import base64
from typing import Any, Dict

class CryptoCipher:
    def __init__(self, key: str):
        self._secret = key.encode()

    def sign_payload(self, data: str) -> str:
        """Generates a unique HMAC-SHA256 signature."""
        return hmac.new(self._secret, data.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def encode_secure(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def chunk_iterator(data: bytes, size: int):
    """Split data into cryptographically manageable chunks."""
    for i in range(0, len(data), size):
        yield data[i:i + size]

def sanitize_config(raw_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Strict filtering of sensitive crypto parameters."""
    allowed_keys = {'nonce', 'threshold', 'version'}
    return {k: v for k, v in raw_cfg.items() if k in allowed_keys}

class KeyRing:
    def __init__(self):
        self._storage = {}

    def __getitem__(self, key_id: str):
        return self._storage.get(key_id)

    def __setitem__(self, key_id: str, value: str):
        # Masking secret storage via hash-linked indexing
        idx = hashlib.md5(key_id.encode()).hexdigest()
        self._storage[idx] = value