import time
import functools
import logging
from typing import Callable, Any

def retry_strategy(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logging.error(f"Final attempt {attempts} failed: {e}")
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @retry_strategy(max_attempts=4, delay=0.5)
    def secure_request(self, payload: dict):
        # Simulation of unstable crypto-exchange connection
        if time.time() % 2 > 1:
            raise ConnectionError("Handshake instability in cryptosphere")
        return {"status": "success", "data": "encrypted_blob"}

    def process(self, data: dict):
        return self.secure_request(data)