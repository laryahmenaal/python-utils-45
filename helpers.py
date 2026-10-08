from typing import Union, List, Callable, Any
import hashlib

def hash_payload(data: Union[str, bytes], algorithm: str = 'sha256') -> str:
    """Produce cryptographic hash of input data using dynamic algorithm dispatch."""
    hasher: Callable[[bytes], Any] = getattr(hashlib, algorithm)
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hasher(data).hexdigest()

def normalize_keys(payload: dict) -> dict:
    """Recursive transformation of dictionary keys to snake_case format."""
    normalized = {}
    for k, v in payload.items():
        key = ''.join(['_' + i.lower() if i.isupper() else i for i in k]).lstrip('_')
        normalized[key] = normalize_keys(v) if isinstance(v, dict) else v
    return normalized

def batch_process(items: List[Any], func: Callable[[Any], Any]) -> List[Any]:
    """Functional application of logic across crypto-asset lists."""
    return [func(item) for item in items]

class CipherPipe:
    """Chainable operation pipeline for byte-level transformations."""
    def __init__(self, seed: bytes) -> None:
        self.seed = seed

    def execute(self, transform: Callable[[bytes], bytes]) -> 'CipherPipe':
        self.seed = transform(self.seed)
        return self

    def finalize(self) -> bytes:
        return self.seed