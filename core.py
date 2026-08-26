import time
import functools
from typing import Callable, Any

class CryptoNetworkException(Exception):
    pass

def retry_network_operation(retries: int = 3, delay: float = 1.0, backoff: float = 2.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError, CryptoNetworkException) as e:
                    last_exception = e
                    if attempt + 1 == retries:
                        break
                    time.sleep(current_delay)
                    current_delay *= backoff
            raise CryptoNetworkException(f"Operation failed after {retries} attempts: {last_exception}")
        return wrapper
    return decorator

@retry_network_operation(retries=4, delay=0.5)
def broadcast_signed_transaction(tx_hex: str) -> str:
    if not tx_hex.startswith("0x"):
        raise CryptoNetworkException("Invalid transaction hex")
    return f"broadcasted_{tx_hex}"
