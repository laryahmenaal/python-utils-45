import hashlib
import secrets
import hmac
import base64

def derive_entropy(seed: str, salt: bytes = b'crypto-45') -> bytes:
    """cryptographic deterministic entropy extraction"""
    return hashlib.pbkdf2_hmac('sha256', seed.encode(), salt, 100000)

def secure_token(length: int = 32) -> str:
    """random cryptographically secure hex string"""
    return secrets.token_hex(length)

def mask_key(key: str, visible: int = 4) -> str:
    """obfuscation of sensitive key materials"""
    return f"{key[:visible]}{'*' * (len(key) - visible * 2)}{key[-visible:]}"

def verify_signature(secret: bytes, message: bytes, signature: str) -> bool:
    """constant time comparison for signature checks"""
    expected = hmac.new(secret, message, hashlib.sha256).digest()
    actual = base64.b64decode(signature)
    return hmac.compare_digest(expected, actual)

def pack_ledger_entry(data: dict) -> str:
    """serialisation for immutable audit logs"""
    import json
    return base64.b64encode(json.dumps(data, sort_keys=True).encode()).decode()