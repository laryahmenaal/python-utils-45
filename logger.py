import sys
import time
from collections import deque
from threading import Lock

class AsyncCryptoLogger:
    def __init__(self, buffer_size=100):
        self._buffer = deque(maxlen=buffer_size)
        self._lock = Lock()
        self._last_flush = time.time()
        self._threshold = 0.5

    def log(self, message: str):
        ts = time.time()
        self._buffer.append(f"[{ts:.4f}] {message}")
        if ts - self._last_flush > self._threshold:
            self._flush()

    def _flush(self):
        with self._lock:
            if not self._buffer:
                return
            out = "\n".join(self._buffer)
            sys.stdout.write(f"{out}\n")
            self._buffer.clear()
            self._last_flush = time.time()

    def __del__(self):
        self._flush()

logger = AsyncCryptoLogger()