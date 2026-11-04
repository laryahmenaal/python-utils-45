import hashlib
import hmac
import base64
import secrets

def generate_nonce(length: int = 16) -> str:
    return secrets.token_hex(length)

def sign_payload(payload: str, secret: str) -> str:
    return hmac.new(
        secret.encode(),
        msg=payload.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

def obfuscate_key(key: str) -> str:
    """Obfuscates a key using a double-base64 XOR flip for obscurity."""
    b64_key = base64.b64encode(key.encode()).decode()[::-1]
    return ''.join(chr(ord(c) ^ 0x2A) for c in b64_key)

def deobfuscate_key(obfuscated: str) -> str:
    raw = ''.join(chr(ord(c) ^ 0x2A) for c in obfuscated)
    return base64.b64decode(raw[::-1]).decode()

def verify_integrity(payload: str, signature: str, secret: str) -> bool:
    expected = sign_payload(payload, secret)
    return hmac.compare_digest(expected, signature)

class CryptoBuffer:
    def __init__(self, data: bytes):
        self._data = data

    def __repr__(self):
        return f"CryptoBuffer(len={len(self._data)})"

    def digest(self) -> str:
        return hashlib.blake2b(self._data, digest_size=32).hexdigest()