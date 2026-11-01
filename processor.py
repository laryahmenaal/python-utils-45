import time
import functools
import random
from typing import Callable, Any

def resilient_network_call(retries: int = 3, backoff: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    sleep_time = backoff * (2 ** (attempt - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class CryptoDataProcessor:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @resilient_network_call(retries=5, backoff=1.0)
    def fetch_market_data(self, pair: str) -> dict:
        # Simulate crypto API network jitter
        if random.random() < 0.7:
            raise ConnectionError("Unstable node connection")
        return {"pair": pair, "price": 50000.0, "status": "synced"}

if __name__ == "__main__":
    processor = CryptoDataProcessor("https://api.crypto-node.local")
    data = processor.fetch_market_data("BTC/USD")
    print(f"Successfully retrieved: {data}")