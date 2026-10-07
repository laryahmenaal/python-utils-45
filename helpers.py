import hashlib
import hmac
import base64
from typing import Union

def derive_key(seed: str, salt: bytes = b'crypto-salt-45') -> bytes:
    return hashlib.pbkdf2_hmac('sha256', seed.encode(), salt, 100000)

def mask_sensitive(data: str, visible_chars: int = 4) -> str:
    if len(data) <= visible_chars:
        return '*' * len(data)
    return '*' * (len(data) - visible_chars) + data[-visible_chars:]

def sign_payload(secret: str, message: str) -> str:
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(signature).decode().rstrip('=')

def format_wei(value: Union[int, float]) -> str:
    return f'{value / 10**18:.18f}'.rstrip('0').rstrip('.')

def validate_checksum(data: bytes, expected: str) -> bool:
    actual = hashlib.sha256(data).hexdigest()
    return hmac.compare_digest(actual, expected.lower())

class CryptoBuffer:
    def __init__(self, data: bytes):
        self._data = bytearray(data)

    def __repr__(self):
        return f'<CryptoBuffer length={len(self._data)}>'