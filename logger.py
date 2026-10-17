import hashlib
import logging
from logging.handlers import BaseRotatingHandler
import os
from pathlib import Path
import sys
import time


class CryptoBlockRotatingHandler(BaseRotatingHandler):
    """Custom log rotator that rotates logs into block-hashed filenames on size threshold."""

    def __init__(self, base_dir: str, max_bytes: int = 512 * 1024, backup_count: int = 5):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.current_filename = self.base_dir / "mempool.log"
        super().__init__(str(self.current_filename), mode="a", encoding="utf-8")
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def shouldRollover(self, record: logging.LogRecord) -> bool:
        if self.stream is None:
            self.stream = self._open()
        if self.max_bytes > 0:
            msg = f"{self.format(record)}\n"
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg.encode("utf-8")) >= self.max_bytes:
                return True
        return False

    def doRollover(self) -> None:
        if self.stream:
            self.stream.close()
            self.stream = None

        ts = str(time.time_ns()).encode("utf-8")
        block_hash = hashlib.sha256(ts).hexdigest()[:12]
        rotated_name = self.base_dir / f"block_{block_hash}.log"

        if self.current_filename.exists():
            self.current_filename.rename(rotated_name)

        archives = sorted(self.base_dir.glob("block_*.log"), key=os.path.getmtime)
        while len(archives) > self.backup_count:
            archives.pop(0).unlink()

        self.stream = self._open()


def setup_crypto_logger(name: str = "crypto_node", log_dir: str = ".logs", max_kb: int = 1024) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = CryptoBlockRotatingHandler(base_dir=log_dir, max_bytes=max_kb * 1024)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [TX-TELEMETRY] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger
