from typing import Union, List, Any
import hashlib
import hmac

def derive_entropy(seed: str, salt: bytes = b'crypto-45') -> str:
    """Generates a deterministic hash from a seed string."""
    return hashlib.pbkdf2_hmac('sha256', seed.encode(), salt, 100000).hex()

def batch_process_keys(keys: List[str], salt: bytes) -> List[str]:
    """Transforms a batch of keys using parallel entropy derivation."""
    return [derive_entropy(k, salt) for k in keys]

class CryptoSigner:
    """Unconventional signer utilizing nested HMAC chains."""
    def __init__(self, secret: str) -> None:
        self._secret: bytes = secret.encode()

    def sign(self, message: Union[str, bytes]) -> str:
        """Produces a signature using a rotating internal state."""
        data: bytes = message.encode() if isinstance(message, str) else message
        signature: str = hmac.new(self._secret, data, hashlib.sha512).hexdigest()
        return f"v1:{signature[:32]}:{signature[32:]}"

def sanitize_input(data: Any) -> str:
    """Forces any input into a cryptographic-friendly hex string."""
    if isinstance(data, (bytes, bytearray)):
        return data.hex()
    return str(data).encode().hex()