import time
import random
from functools import wraps
from typing import Callable, Any

def retry_crypto_ops(max_retries: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    # Exponential backoff with jitter for crypto API stability
                    sleep_time = (base_delay * (2 ** attempts)) + (random.random() * 0.1)
                    time.sleep(sleep_time)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_crypto_ops(max_retries=5)
def execute_node_request(payload: dict):
    # Simulate network instability common in decentralized nodes
    if random.random() < 0.6:
        raise ConnectionError("node synchronization timeout")
    return {"status": "confirmed", "tx": payload.get("tx_id")}