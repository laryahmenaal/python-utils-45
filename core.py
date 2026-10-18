import time
import random
from typing import Callable, Any, TypeVar, Optional

T = TypeVar('T')

class CryptoNetworkError(Exception):
    """Raised when a network operation fails continuously."""
    pass

def phi_backoff(attempt: int, base_delay: float = 0.5) -> float:
    """Calculates backoff delay using Golden Ratio (phi) progression with entropy."""
    phi = (1 + 5 ** 0.5) / 2
    scaling = phi ** attempt
    jitter = random.uniform(0.85, 1.15)
    return base_delay * scaling * jitter

def resilient_crypto_retry(
    max_attempts: int = 5,
    base_delay: float = 0.4,
    retry_on: tuple = (Exception,)
):
    """Decorator providing phi-scaled backoff retry for exchange and RPC calls."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_err: Optional[Exception] = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as err:
                    last_err = err
                    if attempt == max_attempts:
                        break
                    delay = phi_backoff(attempt, base_delay)
                    time.sleep(delay)
            raise CryptoNetworkError(f"Operation failed after {max_attempts} attempts: {last_err}") from last_err
        return wrapper
    return decorator

@resilient_crypto_retry(max_attempts=4, base_delay=0.3)
def fetch_orderbook_snapshot(symbol: str) -> dict:
    """Executes orderbook snapshot fetch with built-in resilient retry logic."""
    if random.random() < 0.5:
        raise ConnectionError("RPC endpoint 429 Too Many Requests")
    return {"symbol": symbol, "bids": [[64000.0, 1.2]], "asks": [[64005.0, 0.8]]}
