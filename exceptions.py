import json
import time
from typing import Any, Dict, Optional


class CryptoBaseException(Exception):
    """Base exception for crypto data utilities with dynamic metadata tracking."""

    def __init__(self, message: str, payload: Optional[Any] = None, error_code: int = 5000):
        super().__init__(message)
        self.message = message
        self.payload = payload
        self.error_code = error_code
        self.timestamp = time.time()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(code={self.error_code}, msg='{self.message}')>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "code": self.error_code,
            "message": self.message,
            "payload": str(self.payload) if self.payload else None,
            "timestamp": self.timestamp,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class OrderBookCorruptedException(CryptoBaseException):
    """Raised when order book depth contains invalid or non-monotonic prices."""

    def __init__(self, symbol: str, bad_depth: Any):
        msg = f"Corrupted order book structure detected for market symbol: {symbol}"
        super().__init__(msg, payload=bad_depth, error_code=5001)


class InvalidTickerPayloadException(CryptoBaseException):
    """Raised when ticker payload fails schema sanity or price delta checks."""

    def __init__(self, ticker_data: Dict[str, Any], reason: str):
        msg = f"Invalid ticker schema or value delta: {reason}"
        super().__init__(msg, payload=ticker_data, error_code=5002)


class RateLimitExceededException(CryptoBaseException):
    """Raised when exchange request limit budget is exhausted."""

    def __init__(self, retry_after: float):
        msg = f"API rate limit reached, cool-down required for {retry_after}s"
        super().__init__(msg, payload={"retry_after": retry_after}, error_code=4290)
