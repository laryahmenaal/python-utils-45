import logging
import sys
from typing import Any, Optional

class CryptoLogger:
    """Custom logger for crypto-related transaction logging."""

    def __init__(self, name: str = "crypto_node", level: int = logging.INFO) -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def log_event(self, event_type: str, data: Any, severity: str = "info") -> None:
        """Standardized gateway for logging sensitive or operational events."""
        message: str = f"[{event_type.upper()}] payload: {str(data)[:100]}"
        getattr(self.logger, severity.lower(), self.logger.info)(message)

    def audit_signature(self, tx_id: str, verified: bool) -> None:
        """Specialized hook for transaction signature auditing."""
        status: str = "SUCCESS" if verified else "FAILURE"
        self.log_event("audit_sig", f"tx: {tx_id} status: {status}", "warning" if not verified else "info")

def get_logger(name: Optional[str] = None) -> CryptoLogger:
    """Factory method for retrieving singleton-like logger instances."""
    return CryptoLogger(name) if name else CryptoLogger()