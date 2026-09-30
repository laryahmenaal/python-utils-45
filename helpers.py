import time
import functools
from typing import Callable, Any

def exponential_backoff(max_retries: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_exception = e
                    sleep_time = base_delay * (2 ** attempt)
                    time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator

def execute_crypto_request(func: Callable) -> Callable:
    """Higher-order function for resilient network communication."""
    @functools.wraps(func)
    def target(*args, **kwargs):
        strategy = exponential_backoff(max_retries=5, base_delay=0.2)
        return strategy(func)(*args, **kwargs)
    return target