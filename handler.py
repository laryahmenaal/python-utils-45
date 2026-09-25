import time
import functools
import random

class NetworkRetryError(Exception):
    """Custom exception for network failures."""
    pass

def with_exponential_backoff(retries=3, base_delay=1.0, jitter=True):
    """Decorator for resilience in crypto operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        raise NetworkRetryError(f"Failed after {retries} attempts: {e}")
                    
                    # Calculate wait: binary exponential backoff with optional jitter
                    delay = base_delay * (2 ** (attempt - 1))
                    if jitter:
                        delay *= random.uniform(0.5, 1.5)
                    
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@with_exponential_backoff(retries=5)
def broadcast_signed_transaction(tx_data):
    """Simulates unstable network broadcasting."""
    if random.random() < 0.7:
        raise ConnectionError("Node unreachable")
    return {"status": "confirmed", "tx_hash": hash(tx_data)}