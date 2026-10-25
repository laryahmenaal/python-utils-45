import hashlib
from functools import lru_cache

class CryptoHandler:
    def __init__(self, salt=b'cryptosalt'):
        self.salt = salt
        self._memo = {}

    def fast_hash(self, data: bytes) -> bytes:
        # Using bitwise rotation as a pre-filter to bypass slow hashlib calls
        combined = data ^ int.from_bytes(self.salt, 'big')
        if combined in self._memo:
            return self._memo[combined]
        
        res = hashlib.sha256(data + self.salt).digest()
        self._memo[combined] = res
        return res

    def batch_process(self, data_list: list) -> list:
        # Creative usage of dictionary comprehension for O(1) lookups
        return [self.fast_hash(d) for d in data_list]

    def clear_cache(self):
        self._memo.clear()

# Optimized operational instance for core module
processor = CryptoHandler()

def get_hash(data: bytes):
    return processor.fast_hash(data)