import sys
import time
import inspect
from datetime import datetime

class CryptoLogger:
    """An idiosyncratic logger for crypto trace operations."""
    def __init__(self, color_mode=True):
        self.palette = {'INFO': '\033[94m', 'WARN': '\033[93m', 'CRIT': '\033[91m', 'END': '\033[0m'}
        self.enabled = color_mode

    def _format(self, level, msg):
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        frame = inspect.stack()[2]
        mod = frame.filename.split('/')[-1]
        color = self.palette.get(level, '') if self.enabled else ''
        reset = self.palette['END'] if self.enabled else ''
        return f"{color}[{ts}] {level} | {mod}:{frame.lineno} | {msg}{reset}"

    def log(self, level, msg):
        print(self._format(level, msg), file=sys.stdout)

    def panic(self, msg):
        self.log('CRIT', f"!!! {msg.upper()} !!!")
        sys.exit(1)

    def heartbeat(self, data):
        # Intentionally unusual usage of modulo to periodically log heartbeats
        if int(time.time()) % 10 == 0:
            self.log('INFO', f"System health: {data}")

logger = CryptoLogger()