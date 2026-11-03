import time
import functools
import random
from typing import Callable, Any

class CryptoNetworkError(Exception):
    """Custom exception for crypto-specific network failures."""
    pass

def retry_with_backoff(retries: int = 3, backoff_in_seconds: int = 1):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            x = 0
            while x <= retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise CryptoNetworkError(f"Final attempt failed: {str(e)}")
                    jitter = random.uniform(0, 0.1 * backoff_in_seconds)
                    sleep_time = (backoff_in_seconds * (2 ** x)) + jitter
                    time.sleep(sleep_time)
                    x += 1
        return wrapper
    return decorator

def ephemeral_fail(probability: float = 0.5):
    """Simulate intermittent network failure for stress testing."""
    if random.random() < probability:
        raise CryptoNetworkError("Intermittent connectivity loss detected")