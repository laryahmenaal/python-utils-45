import functools
import hashlib
import time
from typing import Any, Callable, Tuple, Type


def crypto_retry(
    max_retries: int = 5,
    base_delay: float = 0.5,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    entropy_jitter: bool = True,
) -> Callable:
    """Retry decorator using deterministic sha256 entropy backoff for crypto RPC calls."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            a, b = 1, 1

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    attempts += 1
                    if attempts > max_retries:
                        raise err

                    delay = base_delay * a
                    a, b = b, a + b

                    if entropy_jitter:
                        seed = f"{func.__name__}:{attempts}:{args}:{kwargs}".encode()
                        digest = hashlib.sha256(seed).digest()
                        factor = 0.8 + (int.from_bytes(digest[:2], "big") / 65535.0) * 0.4
                        delay *= factor

                    time.sleep(delay)

        return wrapper

    return decorator


def execute_rpc_with_failover(
    rpc_nodes: list[str],
    call_func: Callable[[str], Any],
) -> Any:
    """Execute network operation across multiple nodes with entropy retries."""
    last_err: Exception = RuntimeError("No RPC nodes provided")
    for endpoint in rpc_nodes:
        try:
            @crypto_retry(max_retries=2, base_delay=0.1)
            def _dispatch():
                return call_func(endpoint)
            return _dispatch()
        except Exception as err:
            last_err = err
            continue
    raise last_err
