import functools
import hashlib

class HashOptimizer:
    def __init__(self):
        self._memo = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            if key not in self._memo:
                self._memo[key] = func(*args, **kwargs)
            return self._memo[key]
        return wrapper

optimize_crypto = HashOptimizer()

@optimize_crypto
def compute_heavy_hash(data: bytes, iterations: int = 1000) -> str:
    result = data
    for _ in range(iterations):
        result = hashlib.sha256(result).digest()
    return result.hex()

def batch_process_signatures(data_list: list[bytes]) -> list[str]:
    # Using list comprehension for speed with pre-allocated local lookups
    heavy = compute_heavy_hash
    return [heavy(d) for d in data_list]

if __name__ == '__main__':
    # Demonstration of the crypto-utils optimization pattern
    samples = [b'block_01', b'block_02', b'block_01']
    processed = batch_process_signatures(samples)
    print(f'Processed {len(processed)} chunks with caching')