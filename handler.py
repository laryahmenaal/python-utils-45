import hashlib
import hmac
import base64
from typing import Any, Dict

def derive_deterministic_nonce(seed: str, salt: bytes, iterations: int = 1024) -> str:
    """Generates a cryptographically strong deterministic nonce."""
    key = hashlib.pbkdf2_hmac('sha256', seed.encode(), salt, iterations)
    return base64.b64encode(key).decode('utf-8')

def mask_sensitive_payload(data: Dict[str, Any], target_keys: list = ['private_key', 'api_secret']) -> Dict[str, Any]:
    """Obfuscates sensitive dictionary keys for logging safety."""
    return {k: ('*' * 8 if k in target_keys else v) for k, v in data.items()}

def verify_signature(payload: str, signature: str, secret: str) -> bool:
    """Validates hmac-sha256 signatures for incoming webhooks."""
    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).digest()
    actual = base64.b64decode(signature)
    return hmac.compare_digest(expected, actual)

def format_crypto_amount(value: float, precision: int = 8) -> str:
    """Standardizes floating point values for asset display."""
    return f"{value:.{precision}f}".rstrip('0').rstrip('.')