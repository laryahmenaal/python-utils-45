import sys
import time
import collections
from functools import lru_cache

class FastLogger:
    def __init__(self, limit=1000):
        self._buffer = collections.deque(maxlen=limit)
        self._last_flush = time.monotonic()
        self._flush_interval = 2.0

    @lru_cache(maxsize=128)
    def _format_cache(self, level, msg):
        return f"[{time.strftime('%H:%M:%S')}] {level}: {msg}"

    def log(self, level, msg):
        self._buffer.append(self._format_cache(level, msg))
        if time.monotonic() - self._last_flush > self._flush_interval:
            self.flush()

    def flush(self):
        if not self._buffer:
            return
        sys.stdout.write("\n".join(self._buffer) + "\n")
        self._buffer.clear()
        self._last_flush = time.monotonic()

    def __del__(self):
        self.flush()

def get_logger():
    if not hasattr(get_logger, '_instance'):
        get_logger._instance = FastLogger()
    return get_logger._instance