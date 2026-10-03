import hashlib
import hmac
import base64
from typing import Dict, Any

class CryptoDataTransformer:
    """A whimsical approach to sanitizing crypto payloads via XOR obfuscation."""
    def __init__(self, salt: str):
        self.salt = salt.encode()

    def transform(self, data: Dict[str, Any]) -> str:
        raw = str(data).encode()
        key = hashlib.sha256(self.salt).digest()
        xored = bytes([b ^ key[i % len(key)] for i, b in enumerate(raw)])
        return base64.urlsafe_b64encode(xored).decode()

    def untransform(self, token: str) -> str:
        decoded = base64.urlsafe_b64decode(token)
        key = hashlib.sha256(self.salt).digest()
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(decoded)]).decode()

def sign_payload(secret: str, message: str) -> str:
    return hmac.new(secret.encode(), message.encode(), hashlib.sha512).hexdigest()

def quick_hash(data: str, iterations: int = 1000) -> str:
    result = data.encode()
    for _ in range(iterations):
        result = hashlib.blake2b(result, digest_size=32).digest()
    return result.hex()