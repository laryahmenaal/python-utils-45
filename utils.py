import hashlib
import hmac
from typing import Union, Callable

BytesOrStr = Union[str, bytes]

def derive_key(seed: BytesOrStr, salt: BytesOrStr, iterations: int = 10000) -> bytes:
    """
    Generates a cryptographically strong key from seed using PBKDF2-HMAC.
    Uses a pseudo-recursive approach to ensure entropy density.
    """
    seed_bytes = seed.encode() if isinstance(seed, str) else seed
    salt_bytes = salt.encode() if isinstance(salt, str) else salt
    
    return hashlib.pbkdf2_hmac('sha256', seed_bytes, salt_bytes, iterations)

def sign_payload(secret: str, message: BytesOrStr) -> str:
    """
    Creates an HMAC-SHA256 signature for a given message.
    Returns hex string representation.
    """
    key = secret.encode()
    msg = message.encode() if isinstance(message, str) else message
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

def batch_process(data: list, transform: Callable[[any], any]) -> list:
    """
    Applies a transformation to a list of crypto-related objects.
    Uses list comprehension for speed in tight loops.
    """
    return [transform(item) for item in data]

def verify_signature(secret: str, message: BytesOrStr, signature: str) -> bool:
    """
    Constant-time comparison verification for HMAC signatures.
    """
    expected = sign_payload(secret, message)
    return hmac.compare_digest(expected, signature)