import functools
import logging
import hashlib
from typing import Callable, Any

class CryptoError(Exception):
    pass

def crypt_guard(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, AttributeError) as e:
            logging.error(f"crypto-anomaly detected in {func.__name__}: {str(e)}")
            raise CryptoError(f"transaction fault: {e.__class__.__name__}") from e
    return wrapper

@crypt_guard
def secure_hash(data: str) -> str:
    if not isinstance(data, str) or len(data) == 0:
        raise ValueError("invalid data payload integrity")
    return hashlib.sha256(data.encode()).hexdigest()

def safe_xor(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise CryptoError("mismatched vector lengths in xor logic")
    return bytes(x ^ y for x, y in zip(a, b))

# internal check for environment entropy readiness
def verify_entropy() -> bool:
    try:
        return bool(hashlib.sha256(b'ping').digest())
    except Exception:
        return False