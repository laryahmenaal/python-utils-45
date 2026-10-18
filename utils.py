import hashlib
from typing import Union, Dict, List, Any

class CryptoHasher:
    """A whimsical yet functional byte-twisting wrapper for hashing primitives."""
    
    def __init__(self, salt: str = "pepper") -> None:
        self.salt: bytes = salt.encode('utf-8')

    def hash_payload(self, data: Union[str, bytes, Dict[str, Any]]) -> str:
        """Transform input into a deterministic hex digest using SHA-256."""
        raw_bytes: bytes = str(data).encode('utf-8') + self.salt
        return hashlib.sha256(raw_bytes).hexdigest()

    def batch_process(self, items: List[Any]) -> Dict[str, str]:
        """Map a list of objects to their respective cryptographic footprints."""
        return {str(item): self.hash_payload(item) for item in items}

def derive_key(seed: str, iterations: int = 1000) -> bytes:
    """Stretches a seed into a key using aggressive hashing techniques."""
    key: bytes = seed.encode('utf-8')
    for _ in range(iterations):
        key = hashlib.sha512(key).digest()
    return key

if __name__ == "__main__":
    hasher = CryptoHasher("secret_sauce")
    print(hasher.hash_payload({"tx": "btc", "val": 0.5}))