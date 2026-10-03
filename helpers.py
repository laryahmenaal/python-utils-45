import time
import hashlib
import functools
from typing import Callable, Any, Type, Tuple

def crypto_retry(
    max_retries: int = 5,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,)
) -> Callable:
    """
    A retry decorator utilizing Fibonacci backoff combined with a deterministic
    pseudo-random jitter generated from SHA-256 hash of the call signature.
    Optimized for heavily rate-limited crypto RPC nodes.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    # Generate pseudo-random jitter based on attempt state to avoid thundering herd
                    state = f"{func.__name__}-{attempt}-{time.time_ns()}".encode("utf-8")
                    jitter = int(hashlib.sha256(state).hexdigest()[:6], 16) / 16777215.0
                    
                    delay = fib[min(attempt, len(fib) - 1)] + (jitter * 2.0)
                    time.sleep(delay)
        return wrapper
    return decorator
