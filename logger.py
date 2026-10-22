import logging
import sys
from typing import Any, Optional

class CryptoLogger:
    """Custom logger for crypto-related operations."""

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        self._logger: logging.Logger = logging.getLogger(name)
        self._logger.setLevel(level)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def trace(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a high-granularity trace for secret exchange."""
        if self._logger.isEnabledFor(logging.DEBUG - 1):
            self._logger.log(logging.DEBUG - 1, msg, *args, **kwargs)

    def alert(self, msg: str, code: Optional[int] = None) -> None:
        """Urgent logging for security anomaly detection."""
        prefix: str = f"[SECURITY_ALERT {code}] " if code else "[ALERT] "
        self._logger.critical(f"{prefix}{msg}")

    def info(self, msg: str) -> None:
        """Log standard transactional info."""
        self._logger.info(msg)

    def debug(self, msg: str) -> None:
        """Log verbose system state."""
        self._logger.debug(msg)