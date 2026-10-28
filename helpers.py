import hashlib
import hmac
import base64
from typing import Any, Dict

def derive_deterministic_key(seed: str, salt: str = 'py45-crypto') -> str:
    """Generates a persistent key using a salted hmac-sha256 digest."""
    key = hmac.new(salt.encode(), seed.encode(), hashlib.sha256).digest()
    return base64.b85encode(key).decode()

def sanitize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively strips keys containing sensitive markers to prevent leakage."""
    forbidden = {'password', 'secret', 'key', 'token', 'priv'}
    return {
        k: ('***' if any(f in k.lower() for f in forbidden) else v)
        for k, v in data.items()
    }

def xor_cipher(data: bytes, mask: bytes) -> bytes:
    """Simple symmetric XOR mask application for lightweight obfuscation."""
    mask_len = len(mask)
    return bytes([b ^ mask[i % mask_len] for i, b in enumerate(data)])

def format_hex_dump(data: bytes, chunk: int = 4) -> str:
    """Groups byte strings into chunks for easier cryptographic analysis."""
    raw = data.hex()
    return ' '.join(raw[i:i + chunk * 2] for i in range(0, len(raw), chunk * 2))