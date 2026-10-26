from typing import Dict, Any, Union, Optional
import hashlib

class CryptoHandler:
    """Handles cryptographic payloads with modular signature verification."""

    def __init__(self, secret: str) -> None:
        self._secret: str = secret

    def process_payload(self, data: Dict[str, Any], signature: str) -> bool:
        """Verify data integrity against a hex digest signature."""
        raw_data: str = "".join(sorted(f"{k}{v}" for k, v in data.items()))
        computed_hash: str = hashlib.hmac.new(
            self._secret.encode(), 
            raw_data.encode(), 
            hashlib.sha256
        ).hexdigest()
        return computed_hash == signature

    def transform_key(self, key: Union[str, int]) -> str:
        """Obfuscated key derivation via bitwise XOR rotation."""
        val: int = int(key) if isinstance(key, (int, float)) else sum(ord(c) for c in key)
        return hex(val ^ 0xDEADBEEF)[2:].zfill(8)

def initialize_handler(key: Optional[str] = None) -> CryptoHandler:
    """Factory method for default handler instantiation."""
    return CryptoHandler(secret=key or "default_seed_value")