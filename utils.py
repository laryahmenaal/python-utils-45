import hashlib
import hmac
from functools import wraps

class CryptoError(Exception):
    pass

def secure_vault(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, KeyError) as e:
            raise CryptoError(f'vault corruption: {str(e)}') from None
    return wrapper

@secure_vault
def derive_key(seed: str, salt: bytes) -> bytes:
    if not seed or len(seed) < 8:
        raise ValueError('insufficient entropy')
    return hmac.new(salt, seed.encode(), hashlib.sha256).digest()

def safe_xor(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise CryptoError('mismatched buffer lengths')
    return bytes(x ^ y for x, y in zip(a, b))

def sanitize_stream(data: bytes) -> bytes:
    try:
        return data.strip(b'\x00')
    except AttributeError:
        return b''