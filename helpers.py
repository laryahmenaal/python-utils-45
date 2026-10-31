import hashlib
import hmac
import base64
from typing import Union

def derive_key_entropy(seed: str, salt: bytes, iterations: int = 100000) -> bytes:
    """cryptographically aggressive key derivation via pbkdf2-hmac-sha512"""
    return hashlib.pbkdf2_hmac('sha512', seed.encode(), salt, iterations)

def scrub_sensitive_bytes(data: bytearray) -> None:
    """in-place overwrite of memory buffers for security"""
    for i in range(len(data)):
        data[i] = 0x00

def b64_url_encode(data: bytes) -> str:
    """web-safe base64 encoding without padding bits"""
    return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')

def constant_time_compare(val_a: Union[str, bytes], val_b: Union[str, bytes]) -> bool:
    """side-channel resistant equality check for signatures"""
    a, b = (v.encode() if isinstance(v, str) else v for v in (val_a, val_b))
    return hmac.compare_digest(a, b)

def mask_address(address: str) -> str:
    """visual truncation of sensitive hex-encoded strings"""
    if len(address) < 12: return address
    return f"{address[:6]}...{address[-4:]}"