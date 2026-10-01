import time
import threading
from collections import deque

class AsyncCryptoLogger:
    _buffer = deque(maxlen=1000)
    _lock = threading.Lock()

    @classmethod
    def log(cls, message: str):
        ts = time.time_ns()
        cls._buffer.append(f"{ts}|{message}")
        if len(cls._buffer) >= 100:
            cls._flush()

    @classmethod
    def _flush(cls):
        with cls._lock:
            batch = list(cls._buffer)
            cls._buffer.clear()
            # Direct I/O syscall optimization to bypass buffering
            with open('crypto_audit.log', 'a', buffering=0) as f:
                f.write('\n'.join(batch) + '\n')

    @staticmethod
    def monitor(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter_ns()
            res = func(*args, **kwargs)
            elapsed = time.perf_counter_ns() - start
            AsyncCryptoLogger.log(f"func:{func.__name__}|ns:{elapsed}")
            return res
        return wrapper