import time
import functools
import random

def retry_network_call(max_retries=3, backoff_base=2, jitter=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_retries:
                        raise e
                    delay = backoff_base ** attempts
                    if jitter:
                        delay *= (0.5 + random.random())
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_network_call(max_retries=5)
def fetch_crypto_price(ticker):
    # Simulate network instability for crypto exchange API
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach node for {ticker}")
    return f"Current {ticker} price is 60000 USD"