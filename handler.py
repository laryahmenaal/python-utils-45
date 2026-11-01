import hashlib
import hmac
import base64
from typing import Any, Dict

def generate_signature(secret: str, message: str) -> str:
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

def normalize_payload(data: Dict[str, Any]) -> str:
    return ''.join(f'{k}{v}' for k, v in sorted(data.items()))

def verify_integrity(data: Dict[str, Any], secret: str, received_sig: str) -> bool:
    payload = normalize_payload(data)
    expected = generate_signature(secret, payload)
    return hmac.compare_digest(expected, received_sig)

def mask_address(address: str, visible: int = 4) -> str:
    if len(address) <= visible * 2:
        return address
    return f'{address[:visible]}...{address[-visible:]}'

def secure_b64_encode(data: str) -> str:
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

def secure_b64_decode(data: str) -> str:
    padding = '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding).decode()