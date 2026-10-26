import time
import collections
import functools

class CryptoPerformanceLogger:
    def __init__(self, limit=1000):
        self._buffer = collections.deque(maxlen=limit)
        self._registry = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter_ns()
            result = func(*args, **kwargs)
            duration = time.perf_counter_ns() - start
            self._buffer.append((func.__name__, duration))
            if len(self._buffer) >= self._buffer.maxlen:
                self._flush_metrics()
            return result
        return wrapper

    def _flush_metrics(self):
        aggregated = collections.defaultdict(list)
        while self._buffer:
            name, val = self._buffer.popleft()
            aggregated[name].append(val)
        for name, values in aggregated.items():
            self._registry[name] = sum(values) / len(values)

    def get_stats(self):
        return dict(self._registry)

perf_logger = CryptoPerformanceLogger(limit=500)