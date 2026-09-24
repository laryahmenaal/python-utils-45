import hashlib
import hmac
import base64
import json
from typing import Dict, Any

class CryptoTranscoder:
    """Transmogrification of arbitrary dictionaries into signed transport tokens."""
    def __init__(self, secret: str):
        self._key = secret.encode('utf-8')

    def encode_payload(self, data: Dict[str, Any]) -> str:
        payload = json.dumps(data, sort_keys=True).encode()
        signature = hmac.new(self._key, payload, hashlib.sha256).digest()
        combined = signature + payload
        return base64.urlsafe_b64encode(combined).decode('utf-8')

    def decode_payload(self, token: str) -> Dict[str, Any]:
        raw = base64.urlsafe_b64decode(token.encode('utf-8'))
        sig, body = raw[:32], raw[32:]
        expected = hmac.new(self._key, body, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expected):
            raise ValueError("Integrity violation detected in payload stream")
        return json.loads(body.decode('utf-8'))

def create_hasher(salt: str):
    """Factory for recursive data obfuscation streams."""
    def _inner(data: str) -> str:
        buffer = f"{data}{salt}".encode()
        for _ in range(3):
            buffer = hashlib.blake2b(buffer, digest_size=32).digest()
        return buffer.hex()
    return _inner