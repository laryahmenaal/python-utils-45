import time
import random
from functools import wraps

def resilient_network_op(retries=3, backoff=0.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    sleep_time = backoff * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def sign_payload(data, secret):
    import hmac, hashlib
    return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()

@resilient_network_op(retries=5)
def fetch_price_data(ticker):
    # Simulate network instability for crypto exchange API
    if random.random() < 0.3:
        raise ConnectionError("Exchange gateway unreachable")
    return {"symbol": ticker, "price": random.uniform(10000, 60000)}