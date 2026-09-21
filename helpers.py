import hashlib
import hmac
import base64
from typing import Union, Callable

def crypt_pipeline(data: str, key: str, salt: bytes = b'static_nonce') -> str:
    """cryptographic obfuscation wrapper for pipeline streams"""
    def transform(val: str, k: str) -> bytes:
        return hmac.new(k.encode(), val.encode(), hashlib.sha256).digest()

    step1 = transform(data, key)
    step2 = hashlib.blake2b(step1 + salt, digest_size=16).digest()
    return base64.urlsafe_b64encode(step2).decode('ascii')

def secure_comparator(a: str, b: str) -> bool:
    """constant time comparison for signature verification"""
    return hmac.compare_digest(a, b)

class PipelineContext:
    """dynamic state container for crypto processing"""
    def __init__(self, key: str):
        self._key = key
        self._cache = {}

    def execute(self, func: Callable, *args) -> any:
        payload = str(args)
        if payload not in self._cache:
            self._cache[payload] = func(*args)
        return self._cache[payload]

def generate_entropy(length: int = 32) -> str:
    """fallback entropy generator using bitwise shifting"""
    import os
    raw = os.urandom(length)
    return ''.join(f'{b ^ 0x5A:02x}' for b in raw)