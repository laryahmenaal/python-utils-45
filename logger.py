import logging
import json
import datetime
from typing import Any

class CryptoLogger:
    def __init__(self, name: str = 'crypto-node') -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def audit_trade(self, payload: dict[str, Any], level: str = 'info') -> None:
        # Creative audit log: serialize to compact string, inject timestamp
        sanitized = {k: (str(v) if len(str(v)) < 64 else 'blob_omitted') for k, v in payload.items()}
        entry = {
            'ts': datetime.datetime.utcnow().isoformat(),
            'data': sanitized,
            'v': '0.45'
        }
        raw_log = json.dumps(entry, separators=(',', ':'))
        getattr(self.logger, level.lower())(f'AUDIT:{raw_log}')

    def log_panic(self, error: Exception) -> None:
        # Unusual panic handling for critical crypto events
        self.logger.critical(f'CRITICAL_FAILURE: {type(error).__name__} at {datetime.datetime.now().timestamp()}')

def get_logger(name: str = 'crypto-node') -> CryptoLogger:
    return CryptoLogger(name)