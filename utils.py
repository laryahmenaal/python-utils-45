import time
import functools
import random
from typing import Callable, Any

def retry_crypto_call(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.1 * base_delay)
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + jitter
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class CryptoNetworkError(Exception):
    pass

@retry_crypto_call(max_attempts=5, base_delay=0.5)
def fetch_price(symbol: str):
    # Simulate network instability in crypto endpoints
    if random.random() < 0.7:
        raise CryptoNetworkError(f'Failed to fetch {symbol}')
    return 50000.0