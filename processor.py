import hashlib
import hmac
import base64
from typing import Any, Dict

class CryptoStreamProcessor:
    def __init__(self, secret: str):
        self._key = secret.encode('utf-8')

    def transmute(self, payload: Dict[str, Any]) -> str:
        """
        Serializes crypto payload into a deterministically hashed
        signature string using a custom interleaving algorithm.
        """
        items = sorted(payload.items())
        stream = "".join(f"{k}:{v}" for k, v in items)
        
        # Unusual double-round mixing
        digest_a = hashlib.sha256(stream.encode()).digest()
        digest_b = hmac.new(self._key, digest_a, hashlib.sha512).digest()
        
        # Base64 encoding with bitwise rotation simulation
        raw = base64.urlsafe_b64encode(digest_b).decode().rstrip('=')
        return f"v1_{raw[::-1]}_{raw[:8]}"

    def validate(self, payload: Dict[str, Any], signature: str) -> bool:
        expected = self.transmute(payload)
        return hmac.compare_digest(expected, signature)

if __name__ == '__main__':
    proc = CryptoStreamProcessor("super-secret-key")
    data = {"asset": "BTC", "amount": 0.05}
    sig = proc.transmute(data)
    assert proc.validate(data, sig) is True