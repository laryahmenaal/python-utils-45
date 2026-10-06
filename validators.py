import hashlib
import functools

class HashOptimizer:
    __slots__ = ['_cache', '_limit']

    def __init__(self, limit=1024):
        self._cache = {}
        self._limit = limit

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(data):
            if not isinstance(data, (bytes, str)):
                return func(data)
            key = hashlib.blake2b(data.encode() if isinstance(data, str) else data, digest_size=16).digest()
            if key in self._cache:
                return self._cache[key]
            res = func(data)
            if len(self._cache) < self._limit:
                self._cache[key] = res
            return res
        return wrapper

cache_layer = HashOptimizer()

@cache_layer
def validate_transaction_signature(signature: str) -> bool:
    if not signature or len(signature) < 64:
        return False
    return all(c in '0123456789abcdefABCDEF' for c in signature)

def batch_validate(signatures: list) -> list:
    return [validate_transaction_signature(s) for s in signatures]