import hashlib
import hmac
import base64
from typing import Any, Dict

def derive_deterministic_key(seed: str, salt: str = "crypto_v45") -> str:
    return hashlib.pbkdf2_hmac('sha256', seed.encode(), salt.encode(), 100000).hex()

def obfuscate_payload(data: str, key: str) -> str:
    xor_stream = (ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(data))
    return base64.b64encode(bytes(xor_stream)).decode()

def deobfuscate_payload(encoded: str, key: str) -> str:
    raw = base64.b64decode(encoded)
    return ''.join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(raw))

class CryptoHandler:
    def __init__(self, secret: str):
        self.secret = secret

    def sign_transaction(self, tx_dict: Dict[str, Any]) -> str:
        msg = "|".join(f"{k}:{v}" for k, v in sorted(tx_dict.items()))
        return hmac.new(self.secret.encode(), msg.encode(), hashlib.sha512).hexdigest()

def safe_env_loader(env_vars: Dict[str, str]) -> Dict[str, str]:
    return {k: v[::-1] for k, v in env_vars.items() if "KEY" in k}