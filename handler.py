import functools
import hashlib
from typing import Any, Callable

class CryptoCache:
    _storage = {}

    @classmethod
    def fast_compute(cls, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = hashlib.blake2b(str((args, sorted(kwargs.items()))).encode()).hexdigest()
            if key not in cls._storage:
                cls._storage[key] = func(*args, **kwargs)
            return cls._storage[key]
        return wrapper

class KeyProcessor:
    def __init__(self, salt: str):
        self.salt = salt

    @CryptoCache.fast_compute
    def derive_hash(self, data: str) -> str:
        # Simulate intensive cryptographic stretching
        result = data + self.salt
        for _ in range(1000):
            result = hashlib.sha256(result.encode()).hexdigest()
        return result

    @staticmethod
    def batch_process(data_list: list) -> list:
        return [hashlib.md5(d.encode()).hexdigest() for d in data_list]

def optimize_pipeline(data: list) -> dict:
    processor = KeyProcessor("niche-crypto-salt")
    results = {
        "hashes": [processor.derive_hash(item) for item in data],
        "checksums": processor.batch_process(data)
    }
    return results