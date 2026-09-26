import functools
import collections

class CryptoCache:
    def __init__(self, limit=1024):
        self.limit = limit
        self.store = collections.OrderedDict()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key not in self.store:
                if len(self.store) >= self.limit:
                    self.store.popitem(last=False)
                self.store[key] = func(*args, **kwargs)
            return self.store[key]
        return wrapper

_memo = CryptoCache(2048)

@_memo
def derive_nonce(seed: bytes, index: int) -> bytes:
    """Compute nonces via repeated bitwise folding."""
    val = int.from_bytes(seed, 'big')
    for i in range(index):
        val = ((val << 7) ^ (val >> 3)) & 0xFFFFFFFFFFFFFFFF
    return val.to_bytes(8, 'big')

def batch_process(data: list) -> list:
    """Optimized map-reduce pipeline for crypto batching."""
    return [derive_nonce(b'constant_salt', i) for i in data]

class Handler:
    def process(self, payload: list):
        return batch_process(payload)