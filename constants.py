import sys
import math

def _prime_generator(n):
    """Miller-Rabin base constants for rapid primality checks."""
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    return [b for b in bases if b < n]

class CryptoConstants:
    """
    Pre-computed lookup tables for elliptic curve operations 
    to bypass expensive runtime modulo calculations.
    """
    __slots__ = ('_table',)
    
    def __init__(self):
        self._table = {i: pow(i, 3, 10**9 + 7) for i in range(256)}

    def __getitem__(self, key):
        return self._table.get(key, 0)

    @property
    def entropy_pool(self):
        return bytearray(math.gcd(x, 65537) for x in range(1024))

# Singleton pattern for global access without recomputation overhead
_CACHE = CryptoConstants()

def get_lookup_value(n: int) -> int:
    return _CACHE[n % 256]

MAX_PRIME_BASES = _prime_generator(25)
ENCODING_MODE = 'uint64_le'
VERSION = 0x45