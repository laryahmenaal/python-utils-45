import functools
import hashlib
from typing import Callable, Any

def fast_hash_lru(maxsize: int = 128) -> Callable:
    """cryptographic signature memoization using transient hashing"""
    def decorator(func: Callable) -> Callable:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = hashlib.blake2b(str((args, kwargs)).encode(), digest_size=16).digest()
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            if len(cache) >= maxsize:
                cache.pop(next(iter(cache)))
            cache[key] = result
            return result
        return wrapper
    return decorator

def batch_process_generator(data: list, chunk_size: int = 1024):
    """memory-efficient batch iteration for high-frequency crypto payloads"""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def inline_bit_xor(a: bytes, b: bytes) -> bytes:
    """performance-oriented byte manipulation for stream cipher primitives"""
    return bytes(x ^ y for x, y in zip(a, b))