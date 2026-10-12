import time
import functools
import random

def retry_network_ops(retries=3, base_delay=1.0, jitter=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = base_delay * (2 ** attempt) + (random.random() * jitter)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@retry_network_ops(retries=3)
def fetch_crypto_price(ticker):
    # Simulate network instability for crypto API
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach node for {ticker}")
    return {"symbol": ticker, "price": 50000.0}

if __name__ == "__main__":
    try:
        data = fetch_crypto_price("BTC")
        print(f"Success: {data}")
    except Exception as e:
        print(f"Operation failed after retries: {e}")