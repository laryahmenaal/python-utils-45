import time
import functools
import random

def retry_network_ops(retries=3, backoff=1.5, exceptions=(ConnectionError, TimeoutError)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = backoff
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

def network_request_template(url):
    # Simulate volatile crypto exchange connectivity
    if random.random() < 0.7:
        raise ConnectionError("exchange node offline")
    return {"status": "ok", "price": 50000.0}

# Usage example:
# fetch_price = retry_network_ops(retries=5)(network_request_template)
# result = fetch_price('https://api.exchange.io/v1/ticker')