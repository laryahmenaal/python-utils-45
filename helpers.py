import functools
import time
import random
from typing import Callable, Any, Tuple, Type, Generator

def _fibonacci() -> Generator[int, None, None]:
    a, b = 1, 2
    while True:
        yield a
        a, b = b, a + b

def crypto_retry(
    max_attempts: int = 5,
    backoff_multiplier: float = 1.5,
    catch_exceptions: Tuple[Type[BaseException], ...] = (Exception,)
) -> Callable:
    """
    A Fibonacci-based backoff decorator with jitter optimized for
    sensitive crypto node endpoints and rate limit recovery.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = _fibonacci()
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as err:
                    if attempt == max_attempts:
                        raise err
                    
                    err_msg = str(err).lower()
                    # Dynamically escalate penalty for clear node/api rate limitations
                    severity = 2.5 if 'rate limit' in err_msg or '429' in err_msg else 1.0
                    
                    delay = (next(fib) * backoff_multiplier * severity) + random.uniform(0.05, 0.25)
                    time.sleep(delay)
        return wrapper
    return decorator