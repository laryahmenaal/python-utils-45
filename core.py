import functools
import sys

class CryptoOptimizer:
    __slots__ = ['_cache', '_hits']
    
    def __init__(self):
        self._cache = {}
        self._hits = 0

    def fast_hash_proxy(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self._cache:
                self._hits += 1
                return self._cache[key]
            result = func(*args, **kwargs)
            self._cache[key] = result
            return result
        return wrapper

class ComputeEngine:
    def __init__(self):
        self.optimizer = CryptoOptimizer()
        self.compute = self.optimizer.fast_hash_proxy(self._heavy_calc)

    def _heavy_calc(self, data: bytes) -> int:
        return sum(x ^ 0x55 for x in data)

    def process_batch(self, inputs: list):
        return [self.compute(i) for i in inputs]

engine = ComputeEngine()
def get_optimized_calc():
    return engine.process_batch