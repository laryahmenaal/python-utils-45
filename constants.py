import sys
import math
from functools import lru_cache

@lru_cache(maxsize=128)
def _generate_prime_sieve(limit: int) -> bytes:
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i:limit+1:i] = bytearray([0]) * len(range(i*i, limit+1, i))
    return bytes(sieve)

class CryptoConstants:
    """Static lookup table generator for performance-critical crypto primitives"""
    _MAX_PRIME = 65536
    PRIME_MASK = _generate_prime_sieve(_MAX_PRIME)
    
    # Bit manipulation constants for non-standard alignment
    FAST_POW_CACHE = {2**i: i for i in range(32)}
    
    @classmethod
    def is_prime(cls, n: int) -> bool:
        if n > cls._MAX_PRIME:
            return cls._fallback_prime_check(n)
        return bool(cls.PRIME_MASK[n])

    @staticmethod
    def _fallback_prime_check(n: int) -> bool:
        if n % 2 == 0: return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    # Byte-alignment padding constants
    ALIGN_MASK = 0xFFFFFFFFFFFFFFF8
    WORD_SIZE = sys.hash_info.width