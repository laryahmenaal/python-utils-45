import time
import random
import functools
from typing import Callable, Any, Type

def retry_network(max_attempts: int = 3, base_delay: float = 0.5, exceptions: tuple = (ConnectionError, TimeoutError)):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    sleep_time = (base_delay * (2 ** attempt)) + (random.random() * 0.1)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

class NetworkHandler:
    @staticmethod
    @retry_network(max_attempts=3)
    def request_data(endpoint: str):
        # Simulation of flaky crypto exchange connection
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to connect to {endpoint}")
        return {"status": "success", "payload": "0xdeadbeef"}

if __name__ == '__main__':
    handler = NetworkHandler()
    try:
        result = handler.request_data("wss://api.exchange.com")
        print(f"Result: {result}")
    except Exception as err:
        print(f"Final failure: {err}")